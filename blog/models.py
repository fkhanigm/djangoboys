from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), db_index=True, unique=True)
    text = models.TextField(_('Text'))
    created_date = models.DateTimeField(_('Create date'), auto_now_add=True)
    update_date = models.DateTimeField(_("Update at"), auto_now=True)
    published_date = models.DateTimeField(_('Publish date'), db_index=True)
    draft = models.BooleanField(_('Draft'), default=True, db_index=True)
    image_title = models.ImageField(_('Image'), upload_to='post/images')
    #tag = models.JSONField(null=True, blank=True, db_index=True)
    category = models.ForeignKey(
        'Category', 
        related_name='posts',
        verbose_name=_("Category"), 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
        )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name="Author",
        related_name='posts',
        related_query_name='children'
        )
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-published_date']

    def __str__(self):
        return self.title
    
    def create_setting(self, comment=True, author=True, allow_discussion=False):
        return PostSetting.objects.create(
            post=self, comment=comment, author=author, allow_discussion=allow_discussion
        )

    def get_comments(self):
        comments = []
        for com in self.comments.filter(parent=None):
            comments.append(
                (com, com.children.all())
            )
        return comments

    @property

    def comment_count(self):#means Comment.objects.filter(post=self).count()
        q = self.comments.all()
        return q.count()

    @property
    def convert_publish_date(self):
        converted_date = f"{self.published_date.day} - {self.published_date.month} - {self.published_date.year}"
        return converted_date

    @property
    def convert_create_date(self):
        converted_date = f"{self.create_date.day} - {self.create_date.month} - {self.created_date.year}"
        return converted_date



class PostSetting(models.Model):
    post = models.OneToOneField(
        Post, verbose_name=_("post"), related_name='post_setting', related_query_name='post_setting',
        on_delete=models.CASCADE)
    comment = models.BooleanField(_("comment"))
    author = models.BooleanField(_("author"))
    allow_discussion = models.BooleanField(_("allow discussion"))
    
    class Meta:
        verbose_name = _("PostSetting")
        verbose_name_plural = _("PostSettings")


class Category(models.Model):
    name = models.CharField(_("Category"), max_length=50)
    slug = models.SlugField(_('Slug'), null=True)
    parent = models.ForeignKey(
        "self", 
        verbose_name=_("Parent"), 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='children', 
        related_query_name='children'
        )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_children(self):
        return self.children.all()

class LikeComment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'), 
        on_delete=models.CASCADE)
    comment = models.ForeignKey(
        'blog.comment',
        verbose_name=_('Comment'),
        related_query_name=_('LikeComment'),
        related_name=_('LikeComment'),
        on_delete=models.CASCADE)
    condition = models.BooleanField(_("Condition")),
    create_date = models.DateTimeField(_("Created date"), auto_now_add=True),
    update_date = models.DateTimeField(_("Update date"), auto_now=True)

    class Meta:
        unique_together = [['author', 'comment']]#for limited user to like any comment one time
        verbose_name = _('LikeComment')
        verbose_name_plural = _('LikeComments')

    def __str__(self):
        return str(self.condition)


class Comment(models.Model):
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE, 
        related_name='comments', 
        related_query_name='comments', 
        verbose_name=_("Post"), 
        )#, related_name='comments'
    #The related_name attribute allows us to name the attribute that we use for the 
    # relation from the related object back to this one. After defining this, we can 
    # retrieve the post of a comment object using comment.post and retrieve all comments 
    # of a post using post.comments.all() . If you don’t define the related_name attribute, 
    # Django will use the name of the model in lowercase, followed by _set (that is, 
    # comment_set ) to name the manager of the related object back to this one.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
        )
    ##related_name='Comment', related_query_name='Comment'
    text = models.TextField(_('Text'))
    created_date = models.DateTimeField(
        _('Create date'), 
        default=timezone.now
        )
    update_date = models.DateTimeField(
        _('Update date'), 
        default=timezone.now
        )
    is_confirmed = models.BooleanField(_("Confirm"), default=True)
    parent = models.ForeignKey(
        'self', 
        verbose_name=_('parent'), 
        null=True,
        on_delete=models.CASCADE, 
        blank=True,
        related_name='children', 
        related_query_name='child'
        )


#    def approve(self):
#        self.is_confirmed = True
#        self.save()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created_date']
    
    def __str__(self):
        return self.post.title

    @property
    def like_count(self):
        q = LikeComment.objects.filter(comment=self, condition=True)
        return q.count()

    @property
    def dis_like_count(self):
        q = LikeComment.objects.filter(condition=False)
        return q.count()
        
    @property
    def convert_create_date(self):
        converted_date = f"{self.create_date.day} - {self.create_date.month} - {self.create_date.year}"
        return converted_date
