from django import template

register = template.Library()

@register.inclusion_tag("review/_list.html", takes_context=True)
def reviews_template(context):

    post = context["post"]
    reviews = post.review_set.all()

    context.update({
        "reviews": reviews,
    })
    return context