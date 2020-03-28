from ariadne import ObjectType
from ariadne.types import GraphQLResolveInfo
from more_itertools import first_true

comment = ObjectType("Comment")


@comment.field("author")
def resolve_comment_author(parent: dict, info: GraphQLResolveInfo):
    return first_true(
        info.context['db'].users,
        None,
        lambda usr: usr['id'] == parent['author']
    )


@comment.field("post")
def resolve_comment_post(parent: dict, info: GraphQLResolveInfo):
    return first_true(
        info.context['db'].users,
        None,
        lambda pst: pst['id'] == parent['post']
    )
