from django.shortcuts import render, get_object_or_404
from blog.models import Comment, Post, Tag


def serialize_post(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [tag.title for tag in post.tags.all()],
    }


def serialize_posts_for_side_block(post):
    return {'title': post.title,
            'author': post.author.username,
            'published_at': post.published_at,
            'slug': post.slug
            }


def serialize_most_popular_posts(post):
    return {'title': post.title,
            'published_at': post.published_at,
            'slug': post.slug,
            'first_tag_title': post.tags.first().title
            }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts_count,
    }


def index(request):
    most_popular_posts = Post.objects.popular()[:5].prefetch_related('tags')
    most_fresh_posts = Post.objects.order_by('published_at')[:5]. \
        prefetch_related('author', 'tags'). \
        fetch_with_comments_count()

    most_popular_tags = Tag.objects.popular()[:5].prefetch_related('posts')

    context = {
        'most_popular_posts': [serialize_most_popular_posts(post) for post in most_popular_posts],
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post).prefetch_related('author')
    serialized_comments = [
        {
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        } for comment in comments
    ]
    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes.count(),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [tag.title for tag in post.tags.all()],
    }

    most_popular_tags = Tag.objects.popular()[:5]
    most_popular_posts = Post.objects.popular()[:5].prefetch_related('author')

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [serialize_posts_for_side_block(post) for post in most_popular_posts]
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = get_object_or_404(Tag, title=tag_title.lower())
    most_popular_tags = Tag.objects.popular()[:5]

    posts = Post.objects
    most_popular_posts = posts.popular()[:5].prefetch_related('author')
    related_posts = posts.filter(tags__title__contains=tag_title). \
                        prefetch_related('author', 'tags')[:20]. \
        fetch_with_comments_count()

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [serialize_posts_for_side_block(post) for post in most_popular_posts]
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
