from . import db
from .models import User,Workouts
from flask import Blueprint,render_template,url_for,request,redirect,flash
from flask_login import login_required,current_user
main =Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html',title='home')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',title='profile',name=current_user.name )

@main.route('/new-workout')
@login_required
def new_workout():
    return render_template('create_workout.html')

@main.route('/new-workout',methods=['GET','POST'])
@login_required
def new_workout_post():
    workout_name=request.form.get('workout_name')
    sets=request.form.get('sets')
    workouts=Workouts(workout_name=workout_name,sets=sets,user=current_user)
    db.session.add(workouts)
    db.session.commit()

    flash('your workout as been added!','success')

    return render_template('create_workout.html')

@main.route('/all')
@login_required
def user_workouts():
    page=request.args.get('page',1,type=int )
    user=User.query.filter_by(email=current_user.email).first_or_404()
    # user = User.query.get(current_user.id)
    # workouts=user.workouts
    workouts=Workouts.query.filter_by(user=user).paginate(page=page,per_page=2)
    
    
    return render_template('all_workouts.html', user=user, workouts=workouts)

@main.route('/workout/<int:workout_id>/update',methods=['GET','POST'])
@login_required
def update_workout(workout_id):
    workout= Workouts.query.get_or_404(workout_id)
    if request.method == 'POST':
        workout.workout_name = request.form['workout_name']
        workout.sets = request.form['sets']
        db.session.commit()
        flash('workout has been updated!','success')
        return redirect(url_for('main.user_workouts'))

    return render_template('update_workout.html',workout=workout)


@main.route('/workout/<int:workout_id>/delete',methods=['GET','POST'])
@login_required
def delete_workout(workout_id):
    workout= Workouts.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash('Successfully Deleted!','success')
    return redirect(url_for('main.user_workouts'))