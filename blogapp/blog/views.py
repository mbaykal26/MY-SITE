from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from blog.models import Blog, Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# from . forms import CommentForm
from django.views.decorators.http import require_POST


# Create your views here.


def index(request):
    context = {
        "blogs" : Blog.objects.filter(is_active=True, is_home=True),
        "categories" : Category.objects.all()
    }
    return render(request, "blog/index.html",context)
    # return HttpResponse("Home Page")


@login_required(login_url="account/login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blogs(request):
    context = {
        "blogs" : Blog.objects.filter(is_active=True),
        "categories": Category.objects.all()
    }
    return render(request, "blog/blogs.html",context)
    # return HttpResponse("Blogs")



def blog_details(request, slug):
        # try:
        #     # blog = get_object_or_404(Blog, status=Blog.Status.PUBLISHED, 
                                     
        #     #         # slug=blog,
        #     #         publish__year=year,
        #     #         publish__month=month,
        #     #         publish__day=day
        #     #     )

        #     # List of active comments for this blog
        #     comments = slug.comments.filter(active=True)
                    
        #     # Form for users to write comment
        #     form = CommentForm()

        # except Blog.DoesNotExist:
        #     raise Http404("No article found.")
    
        # return render(request, 'blog/blog-details.html', {
        #     'blog': slug,
        #     'comments': comments,
        #     'form': form
            
        blog = Blog.objects.get(slug=slug)      
        return render(request, "blog/blog-details.html", {
            "blog": blog
        })
            

    
    
    
    
    # if not  request.user.is_authenticated:
    #     return redirect("account/login")
    # else:
        # blog = Blog.objects.get(slug=slug)
        # return render(request, "blog/blog-details.html", {
        #     "blog": blog
        # })
    #return HttpResponse("Blog Details : " + str(id))
    

def blogs_by_category(request, slug):
    context = {
        "blogs" : Category.objects.get(slug=slug).blog_set.filter(is_active=True),
        # "blogs" : Blog.objects.filter(is_active=True, category__slug=slug),
        "categories" : Category.objects.all(),
        "selected_category" : slug,
    }
    return render(request, "blog/blogs.html",context)


@require_POST
def comment_for_blog(request, blog_id):

    # get the blog by blog_id
    blog = get_object_or_404(Blog, id = blog_id, status=Blog.Status.PUBLISHED)
    comment = None
    
    # A comment form
    form = CommentForm(data=request.POST)

    if form.is_valid():
        # Create a Comment object before saving it to the database
        comment = form.save(commit=False)

        # Assign the blog to the comment
        comment.blog = blog
        # Save the comment to the database
        comment.save()
        pass

    return render(request, 'blog/comment.html', {'blog': blog, 'form': form, 'comment': comment})

    pass