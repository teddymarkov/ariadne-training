from uuid import uuid4

from ariadne import MutationType
from ariadne.types import GraphQLResolveInfo

mutation = MutationType()


@mutation.field("createUser")
def resolve_create_user(_, info: GraphQLResolveInfo, data: dict):
    users = info.context['db'].users

    # Verify email address is free
    if data['email'] in (usr['email'] for usr in users):
        raise ValueError("Email taken.")

    # Create the new user
    usr = {
        'id': uuid4(),
        **data,
    }
    users.append(usr)

    return usr


@mutation.field("updateUser")
def resolve_update_user(_, info, id: str, data: dict):
    name = data.get("name")
    email = data.get("email")
    age = data.get("age", False)
    users = info.context['db'].users
    # Fetch the user
    for usr in users:
        if usr['id'] == id:
            break
    else:
        raise ValueError("User not found")

    # Verify email address is free
    if email:
        if email in (t_usr['email'] for t_usr in users):
            raise ValueError("Email taken.")

    # Update properties
    if name is not None:
        usr['name'] = name
    if email is not None:
        usr['emial'] = email
    if age is not False:
        usr['age'] = age

    return usr


@mutation.field("deleteUser")
def resolve_delete_user(_, info: GraphQLResolveInfo, id: str):
    # Delete the user
    for usr_ind, usr in enumerate(info.context['db'].users):
        if usr['id'] == id:
            del info.context['db'].users[usr_ind]
            break
    else:
        raise ValueError("User not found")

    # Delete user's comments
    comments_dump = list(info.context['db'].comments)  # Use a copy for iter
    for cmt_ind, cmt in enumerate(comments_dump):
        if cmt['author'] == usr['id']:
            del info.context['db'].comments[cmt_ind]
    # Delete user's posts
    cnt = 0
    while cnt < len(info.context['db'].posts):
        if info.context['db'].posts[cnt]['author'] == usr['id']:
            # Delete the comments of the post
            cnt2 = 0
            while cnt2 < len(info.context['db'].comments):
                if info.context['db'].comments[cnt2]['post'] == \
                        info.context['db'].posts[cnt]['id']:
                    del info.context['db'].comments[cnt2]
                else:
                    cnt2 += 1
            # Execute post deletion
            del info.context['db'].posts[cnt]
        else:
            cnt += 1

    return usr


@mutation.field("createPost")
def resolve_create_post(_, info: GraphQLResolveInfo, data: dict):
    if not data['author'] in (usr for usr in info.context['db'].users):
        raise ValueError('Author not found.')
    pst = {
        'id': uuid4(),
        **data,
    }
    info.context['db'].posts.append(pst)
    return pst


@mutation.field("updatePost")
def resolve_update_post(_, info: GraphQLResolveInfo, id: str, data: dict):
    title = data.get("title")
    body = data.get("body")
    published = data.get("published")
    posts = info.context['db'].posts

    # Fetch the post
    for pst in posts:
        if pst['id'] == id:
            break
    else:
        raise ValueError("Post not found")

    # Verify title is unique
    if title:
        if title in (t_pst['title'] for t_pst in posts):
            raise ValueError("Title is already taken.")

    # Update properties
    if title is not None:
        pst['title'] = title
    if body is not None:
        pst['body'] = body
    if published is not None:
        pst['published'] = published

    return pst


@mutation.field("deletePost")
def resolve_delete_post(_, info: GraphQLResolveInfo, id: str):
    # Delete the post
    for pst_ind, pst in enumerate(info.context['db'].posts):
        if pst['id'] == id:
            del info.context['db'].posts[pst_ind]
            break
    else:
        raise ValueError("Post not found")

    # Delete the comments of this post
    cnt = 0
    while cnt < len(info.context['db'].comments):
        if info.context['db'].comments[cnt]['post'] == pst['id']:
            del info.context['db'].comments[cnt]
        else:
            cnt += 1

    return pst


@mutation.field("createComment")
def resolve_create_comment(_, info: GraphQLResolveInfo, data):
    if not data['author'] in (usr['id'] for usr in info.context['db'].users):
        raise ValueError('Author not found.')
    if not data['post'] in (pst['id'] for pst in info.context['db'].posts):
        raise ValueError('Post not found.')
    cmt = {
        'id': uuid4(),
        **data,
    }
    info.context['db'].comments.append(cmt)
    return cmt


@mutation.field("updateComment")
def resolve_update_comment(_, info: GraphQLResolveInfo, id: str, data: dict):
    text = data.get("text")
    comments = info.context['db'].comments
    # Fetch the comment
    for cmt in comments:
        if cmt['id'] == id:
            break
    else:
        raise ValueError("Comment not found")

    # Update properties
    if text is not None:
        cmt['text'] = text

    return cmt


@mutation.field("deleteComment")
def resolve_delete_comment(_, info: GraphQLResolveInfo, id):
    for cmt_ind, cmt in enumerate(info.context['db'].comments):
        if cmt['id'] == id:
            del info.context['db'].comments[cmt_ind]
            break
    else:
        raise ValueError("Comment not found")
    return cmt
