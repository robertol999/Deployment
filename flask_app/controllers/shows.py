from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_app.models.user import User
from flask_app.models.show import Show


@app.route('/shows/new')
def addShow():
    if 'user_id' in session:
        return render_template('addShow.html')
    return redirect('/')

@app.route('/show', methods = ['POST'])
def createShow():
    if 'user_id' not in session:
        return redirect('/')
    if not Show.validate_show(request.form):
        return redirect(request.referrer)
    data = {
        'title': request.form['title'],
        'comment': request.form['comment'],
        'network': request.form['network'],
        'date': request.form['date'],
        'user_id': session['user_id'] # id e personit te loguar
    }
    Show.create(data)
    return redirect('/')


@app.route('/show/<int:id>')
def viewShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
        'show_id': id
    }
    show = Show.get_show_by_id(data)
    if show:
        usersWhoLikes = Show.get_users_who_liked_by_show_id(data)
        return render_template('viewShow.html', show=show, usersWhoLikes= usersWhoLikes)
    return redirect('/')

@app.route('/show/edit/<int:id>')
def editShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    show = Show.get_show_by_id(data)
    if show and show['user_id'] == session['user_id']:
        return render_template('editShow.html', show=show)
    return redirect('/')


@app.route('/show/update/<int:id>', methods = ['POST'])
def updateShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    show = Show.get_show_by_id(data)
    if show and show['user_id'] == session['user_id']:
        if not Show.validate_showUpdate(request.form):
            return redirect(request.referrer)
        data = {
            'comment': request.form['comment'],
            'network': request.form['network'],
            'date': request.form['date'],
            'id': id
        }
        Show.update(data)
        return redirect('/show/'+ str(id))
    return redirect('/')



@app.route('/show/delete/<int:id>')
def deleteShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
    }
    show = Show.get_show_by_id(data)
    if show['user_id'] == session['user_id']:
        Show.delete_all_show_comments(data)
        Show.delete(data)
    return redirect('/')

@app.route('/add/comment/<int:id>', methods = ['POST'])
def addComment(id):
    if 'user_id' not in session:
        return redirect('/')
    if len(request.form['comment'])<2:
        flash('The comment should be at least 2 characters', 'comment')
    data = {
        'comment': request.form['comment'],
        'user_id': session['user_id'],
        'book_id': id
    }
    Show.addComment(data)
    return redirect(request.referrer)

@app.route('/update/comment/<int:id>', methods = ['POST'])
def updateComment(id):
    if 'user_id' not in session:
        return redirect('/')
    if len(request.form['comment'])<2:
        flash('The comment should be at least 2 characters', 'comment')
    data = {
        'comment': request.form['comment'],
        'id': id
    }
    komenti = Show.get_comment_by_id(data)
    if komenti['user_id'] == session['user_id']:
        Show.update_comment(data)
    return redirect('/show/'+ str(komenti['show_id']))

@app.route('/delete/comment/<int:id>')
def deleteComment(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    komenti = Show.get_comment_by_id(data)
    if komenti['user_id'] == session['user_id']:
        Show.delete_comment(data)
    return redirect(request.referrer)



@app.route('/edit/comment/<int:id>')
def editComment(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    commenti = Show.get_comment_by_id(data)
    if commenti['user_id'] == session['user_id']:
        return render_template('editComment.html', commenti = commenti)
    return redirect('/')


@app.route('/add/like/<int:id>')
def addLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'book_id': id,
        'user_id': session['user_id']
    }
    usersWhoLikes = Show.get_users_who_liked_by_show_id(data)
    print(usersWhoLikes)
    if session['user_id'] not in usersWhoLikes:
        Show.addLike(data)
    return redirect(request.referrer)

@app.route('/remove/like/<int:id>')
def removeLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'book_id': id,
        'user_id': session['user_id']
    }
    Show.removeLike(data)
    return redirect(request.referrer)