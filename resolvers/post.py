from ariadne import ObjectType
from ariadne.types import GraphQLResolveInfo
from more_itertools import first_true

post = ObjectType("Post")


@post.field("author")
def resolve_post_author(parent: dict, info: GraphQLResolveInfo):
    return first_true(
        info.context['db'].users,
        None,
        lambda usr: usr['id'] == parent['author']
    )


@post.field("comments")
def resolve_post_comments(parent: dict, info: GraphQLResolveInfo):
    return filter(
        lambda cmt: cmt['post'] == parent['id'],
        info.context['db'].comments
    )
