from ariadne import QueryType, ObjectType, gql, make_executable_schema
from ariadne.asgi import GraphQL

# Demo user data
users = [
    {
        'id': 1,
        'name': 'Teodor',
        'email': 'mail@mail.com',
        'age': 31
    },
    {
        'id': 2,
        'name': 'Daren',
        'email': 'daren@mail.com',
        'age': 31
    },
    {
        'id': 3,
        'name': 'Mike',
        'email': 'mike@mail.com',
        'age': 31
    }
]

posts = [
    {
        'id': 1,
        'title': 'Post title I',
        'body': 'The body of the post.',
        'published': True
    },
    {
        'id': 2,
        'title': 'Post title II',
        'body': 'The body of the post.',
        'published': True
    },
    {
        'id': 3,
        'title': 'Post title III',
        'body': 'The body of the post.',
        'published': False
    }
]


type_defs = gql("""
    type Query {
        me: User!
        post: Post!
        users(name: String): [User!]!
        posts(title: String): [Post!]!
    }

    type Post {
        id: ID!
        title: String!
        body: String!
        published: Boolean!
    }

    type User {
        id: ID!
        name: String!
        email: String!
        age: Int
    }
""")

query = QueryType()
post = ObjectType('Post')
user = ObjectType('User')


@query.field("me")
def resolve_me(*_):
    return {
        'id': '123098',
        'name': 'Mike',
        'email': 'mike@gmail.com'
    }


@query.field("post")
def resolve_post(*_):
    return {
        'id': '4321',
        'title': 'Some title',
        'body': 'Long text.',
        'published': True
    }


@query.field("users")
def resolve_users(*_, name: str = None):
    if name:
        return filter(lambda usr: usr['name'].lower() == name.lower(), users)
    return users


@query.field("posts")
def resolve_posts(*_, title: str = None):
    if title:
        return filter(lambda pst: title.lower() in pst['title'].lower(), posts)
    return posts


schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)
