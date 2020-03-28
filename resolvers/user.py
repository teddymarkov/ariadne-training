from ariadne import ObjectType
from ariadne.types import GraphQLResolveInfo

user = ObjectType("User")


@user.field("posts")
def resolve_user_posts(parent: dict, info: GraphQLResolveInfo):
    return filter(
        lambda pst: pst['author'] == parent['id'],
        info.context['db'].posts
    )


@user.field("comments")
def resolve_user_comments(parent: dict, info: GraphQLResolveInfo):
    return filter(
        lambda cmt: cmt['author'] == parent['id'],
        info.context['db'].comments
    )
