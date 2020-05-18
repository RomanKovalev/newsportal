from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, Permission

from .forms import PostCreateForm, CommentCreateForm
from .models import Post, Comment
from .tasks import send_email_task

class PostsListView(ListView):
    model = Post
    paginate_by = 100
    ordering = ['-created']

    def get_queryset(self, *args, **kwargs):
        qs = self.model.objects.filter(approved='approved')
        return qs




class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    
    def form_valid(self, form):
        if self.request.user.has_perm('auth.can_approve'):
            form.instance.approved = 'approved'
        else:
            form.instance.approved = 'waiting'
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentCreateForm
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        post_pk = self.request.path.split('/')[2]
        post = get_object_or_404(Post, pk=post_pk)
        form.instance.save()
        post.comments.add(form.instance)

        current_site = get_current_site(self.request)
        mail_subject = 'Your post has new reply'
        message = render_to_string('posts/new_comment_email.html', {
            'post': post,
            'content': form.instance.content,
            'author': form.instance.owner,
            'domain': current_site.domain,
        })
        to_email = post.owner.email
        # email = EmailMessage(
        #     mail_subject, message, to=[to_email]
        # )
        # email.send()
        send_email_task.delay(mail_subject, message, to_email)

        return super().form_valid(form)
    
    def get_success_url(self):
        post_pk = self.request.path.split('/')[2]
        return reverse('posts:post-detail', kwargs={'pk': post_pk})


class DashboardView(ListView):
    model = Post
    template_name = "posts/dashboard.html"
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('auth.can_approve'):
            raise PermissionDenied
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super(DashboardView,self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


class ChangePostStatusView(View):

    def get(self, request, pk, status):
        try:
            post = Post.objects.get(pk=pk)
            post.approved = status
            post.save()
        except Exception as e:
            print(e)
        return redirect('posts:dashboard')

class ChangePremoderationModeView(View):

    def get(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
            permission = Permission.objects.get(codename='can_approve')
            if permission in group.permissions.all():
                group.permissions.remove(permission)
            else:
                group.permissions.add(permission)
            group.save()
        except Exception as e:
            print(e)
        return redirect('posts:dashboard')        