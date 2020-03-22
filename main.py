from typing import List, Dict
from uuid import uuid4

from more_itertools import first_true

from ariadne import (
    QueryType,
    MutationType,
    ObjectType,
    gql,
    make_executable_schema,
)
from ariadne.asgi import GraphQL

# Demo user data
users: List[Dict] = [
    {
        'id': "1",
        'name': 'Jack',
        'email': 'jack@mail.com',
        'age': 31,
    },
    {
        'id': "2",
        'name': 'Daren',
        'email': 'daren@mail.com',
        'age': 18,
    },
    {
        'id': "3",
        'name': 'Mike',
        'email': 'mike@mail.com',
        'age': 54,
    },
]

posts: List[Dict] = [
    {
        'id': "1",
        'title': "Et harum quidem rerum",
        'body': "But I must explain to you how all this mistaken idea of "
                "denouncing pleasure and praising pain was born and I will "
                "give you a complete account of the system, and expound the "
                "actual teachings of the great explorer of the truth, the "
                "master-builder of human happiness. No one rejects, dislikes, "
                "or avoids pleasure itself, because it is pleasure, "
                "but because those who do not know how to pursue pleasure "
                "rationally encounter consequences that are extremely painful."
                " Nor again is there anyone who loves or pursues or desires "
                "to obtain pain of itself, because it is pain, but because "
                "occasionally circumstances occur in which toil and pain can "
                "procure him some great pleasure. To take a trivial example, "
                "which of us ever undertakes laborious physical exercise, "
                "except to obtain some advantage from it? But who has any "
                "right to find fault with a man who chooses to enjoy a "
                "pleasure that has no annoying consequences, or one who "
                "avoids a pain that produces no resultant pleasure?",
        'published': True,
        'author': "1",
    },
    {
        'id': "2",
        'title': "In a free hour",
        'body': "At vero eos et accusamus et iusto odio dignissimos ducimus "
                "qui blanditiis praesentium voluptatum deleniti atque "
                "corrupti quos dolores et quas molestias excepturi sint "
                "occaecati cupiditate non provident, similique sunt in "
                "culpa qui officia deserunt mollitia animi, id est laborum "
                "et dolorum fuga. Et harum quidem rerum facilis est et "
                "expedita distinctio. Nam libero tempore, cum soluta nobis "
                "est eligendi optio cumque nihil impedit quo minus id quod "
                "maxime placeat facere possimus, omnis voluptas assumenda "
                "est, omnis dolor repellendus. Temporibus autem quibusdam "
                "et aut officiis debitis aut rerum necessitatibus saepe "
                "eveniet ut et voluptates repudiandae sint et molestiae "
                "non recusandae. Itaque earum rerum hic tenetur a sapiente "
                "delectus, ut aut reiciendis voluptatibus maiores alias "
                "consequatur aut perferendis doloribus asperiores repellat.",
        'published': True,
        'author': "2",
    },
    {
        'id': "3",
        'title': "de Finibus Bonorum et Malorum",
        'body': "On the other hand, we denounce with righteous indignation "
                "and dislike men who are so beguiled and demoralized by the "
                "charms of pleasure of the moment, so blinded by desire, "
                "that they cannot foresee the pain and trouble that are "
                "bound to ensue; and equal blame belongs to those who fail "
                "in their duty through weakness of will, which is the same "
                "as saying through shrinking from toil and pain. These "
                "cases are perfectly simple and easy to distinguish. In a "
                "free hour, when our power of choice is untrammelled and "
                "when nothing prevents our being able to do what we like "
                "best, every pleasure is to be welcomed and every pain "
                "avoided. But in certain circumstances and owing to the "
                "claims of duty or the obligations of business it will "
                "frequently occur that pleasures have to be repudiated and "
                "annoyances accepted. The wise man therefore always holds "
                "in these matters to this principle of selection: he "
                "rejects pleasures to secure other greater pleasures, or "
                "else he endures pains to avoid worse pains.",
        'published': False,
        'author': "2",
    },
]

comments: List[Dict] = [
    {
        'id': "1",
        'text': "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                "sed do eiusmod tempor incididunt ut labore et dolore magna "
                "aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                "ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        'author': "1",
        'post': "1",
    },
    {
        'id': "2",
        'text': "Ut enim ad minima veniam, quis nostrum exercitationem ullam "
                "corporis suscipit laboriosam, nisi ut aliquid ex ea commodi "
                "consequatur?",
        'author': "2",
        'post': "1",
    },
    {
        'id': "3",
        'text': "To take a trivial example, which of us ever undertakes "
                "laborious physical exercise, except to obtain some advantage "
                "from it?",
        'author': "2",
        'post': "1",
    },
    {
        'id': "4",
        'text': "Et harum quidem rerum facilis est et expedita distinctio.",
        'author': "2",
        'post': "2",
    },
]


type_defs = gql("""
    type Query {
        me: User!
        post: Post!
        users(name: String): [User!]!
        posts(title: String): [Post!]!
        comments: [Comment!]!
    }

    type Mutation {
        createUser(data: CreateUserInput): User!
        deleteUser(id: ID!): User!
        createPost(data: CreatePostInput): Post!
        deletePost(id: ID!): User!
        createComment(data: CreateCommentInput): Comment!
        deleteComment(id: ID!): User!
    }
    
    input CreateUserInput {
        name: String!
        email: String!
        age: Int
    }
    
    input CreatePostInput {
        title: String!
        body: String!
        published: Boolean!
        author: ID!
    }
    
    input CreateCommentInput {
        text: String!
        author: ID!
        post: ID!
    }

    type Post {
        id: ID!
        title: String!
        body: String!
        published: Boolean!
        author: User!
        comments: [Comment!]!
    }

    type User {
        id: ID!
        name: String!
        email: String!
        age: Int
        posts: [Post!]!
        comments: [Comment!]!
    }

    type Comment {
        id: ID!
        text: String!
        author: User!
        post: Post!
    }
""")

query = QueryType()
mutation = MutationType()
post = ObjectType("Post")
user = ObjectType("User")
comment = ObjectType("Comment")


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
def resolve_users(*_, name: str = ""):
    if name:
        return filter(
            lambda usr: usr['name'].lower() == name.lower(),
            users
        )
    return users


@query.field("posts")
def resolve_posts(*_, title: str = ""):
    return filter(
        lambda pst: title.lower() in pst['title'].lower(),
        posts
    )


@query.field("comments")
def resolve_comments(*_):
    return comments


@mutation.field("createUser")
def resolve_create_user(*_, data):
    if data['email'] in (usr['email'] for usr in users):
        raise ValueError("Email taken.")
    usr = {
        'id': uuid4(),
        **data,
    }
    users.append(usr)
    return usr


@mutation.field("deleteUser")
def resolve_delete_user(*_, id: str):
    # Delete the user
    for usr_ind, usr in enumerate(users):
        if usr['id'] == id:
            del users[usr_ind]
            break
    else:
        raise ValueError("User not found")

    # Delete user's comments
    comments_dump = list(comments)  # Use a copy for iteration
    for cmt_ind, cmt in enumerate(comments_dump):
        if cmt['author'] == usr['id']:
            del comments[cmt_ind]
    # Delete user's posts
    cnt = 0
    while cnt < len(posts):
        if posts[cnt]['author'] == usr['id']:
            # Delete the comments of the post
            cnt2 = 0
            while cnt2 < len(comments):
                if comments[cnt2]['post'] == posts[cnt]['id']:
                    del comments[cnt2]
                else:
                    cnt2 += 1
            # Execute post deletion
            del posts[cnt]
        else:
            cnt += 1

    return usr


@mutation.field("createPost")
def resolve_create_post(*_, data: dict):
    if not data['author'] in (usr for usr in users):
        raise ValueError('Author not found.')
    pst = {
        'id': uuid4(),
        **data,
    }
    posts.append(pst)
    return pst


@mutation.field("deletePost")
def resolve_delete_post(*_, id: str):
    # Delete the post
    for pst_ind, pst in enumerate(posts):
        if pst['id'] == id:
            del posts[pst_ind]
            break
    else:
        raise ValueError("Post not found")

    # Delete the comments of this post
    cnt = 0
    while cnt < len(comments):
        if comments[cnt]['post'] == pst['id']:
            del comments[cnt]
        else:
            cnt += 1

    return pst


@mutation.field("createComment")
def resolve_create_comment(*_, data):
    if not data['author'] in (usr['id'] for usr in users):
        raise ValueError('Author not found.')
    if not data['post'] in (pst['id'] for pst in posts):
        raise ValueError('Post not found.')
    cmt = {
        'id': uuid4(),
        **data,
    }
    comments.append(cmt)
    return cmt


@mutation.field("deleteComment")
def resolve_delete_comment(*_, id):
    for cmt_ind, cmt in enumerate(comments):
        if cmt['id'] == id:
            del comments[cmt_ind]
            break
    else:
        raise ValueError("Comment not found")
    return cmt


@user.field("posts")
def resolve_user_posts(parent: dict, _):
    return filter(
        lambda pst: pst['author'] == parent['id'],
        posts
    )


@user.field("comments")
def resolve_user_comments(parent: dict, _):
    return filter(
        lambda cmt: cmt['author'] == parent['id'],
        comments
    )


@post.field("author")
def resolve_post_author(parent: dict, _):
    return first_true(
        users,
        None,
        lambda usr: usr['id'] == parent['author']
    )


@post.field("comments")
def resolve_post_comments(parent: dict, _):
    return filter(
        lambda cmt: cmt['post'] == parent['id'],
        comments
    )


@comment.field("author")
def resolve_comment_author(parent: dict, _):
    return first_true(
        users,
        None,
        lambda usr: usr['id'] == parent['author']
    )


@comment.field("post")
def resolve_comment_post(parent: dict, _):
    return first_true(
        users,
        None,
        lambda pst: pst['id'] == parent['post']
    )


schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    user,
    post,
    comment,
)

app = GraphQL(
    schema,
    debug=True
)
