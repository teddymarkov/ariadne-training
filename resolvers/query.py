from ariadne import QueryType
from ariadne.types import GraphQLResolveInfo

query = QueryType()


@query.field("me")
def resolve_me(*_):
    return {
        'id': '123098',
        'name': 'Mike',
        'email': 'mike@gmail.com',
    }


@query.field("post")
def resolve_post(*_):
    return {
        'id': '1',
        'title': 'Some title',
        'body': 'Long text.',
        'published': True,
        'author': '2',
    }


@query.field("users")
def resolve_users(_, info: GraphQLResolveInfo, name: str = ""):
    if name:
        return filter(
            lambda usr: usr['name'].lower() == name.lower(),
            info.context['db'].users
        )
    return info.context['db'].users


@query.field("posts")
def resolve_posts(_, info: GraphQLResolveInfo, title: str = ""):
    return filter(
        lambda pst: title.lower() in pst['title'].lower(),
        info.context['db'].posts
    )


@query.field("comments")
def resolve_comments(_, info: GraphQLResolveInfo):
    return info.context['db'].comments
