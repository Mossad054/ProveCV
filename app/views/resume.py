from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Resume, Template
from app.forms import ResumeForm
import json

# Define a blueprint for resume-related routes
bp = Blueprint('resume', __name__)

@bp.route('/select_template')
@login_required
def select_template():
    # Get all active templates from database
    templates = Template.query.filter_by(is_active=True).all()
    return render_template('resume/select_template.html', templates=templates)

@bp.route('/create_resume/<template_name>', methods=['GET', 'POST'])
@login_required
def create_resume(template_name):
    template = Template.query.get_or_404(template_name)
    form = ResumeForm()
    
    if form.validate_on_submit():
        # Create new resume
        resume = Resume(
            user_id=current_user.id,
            template_name=template_name,
            name=form.name.data,
            content={
                'name': form.name.data,
                'email': form.email.data,
                'phone': form.phone.data,
                'experience': form.experience.data,
                'education': form.education.data,
                'skills': form.skills.data
            }
        )
        db.session.add(resume)
        db.session.commit()
        
        return redirect(url_for('resume.view_resume', resume_id=resume.id))
        
    return render_template('resume/create_resume.html', form=form, template=template)

@bp.route('/view_resumes')
@login_required
def view_resumes():
    # Fetch all resumes for the current user
    user_resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template('view_resumes.html', resumes=user_resumes)

@bp.route('/edit_resume/<int:resume_id>', methods=['GET', 'POST'])
@login_required
def edit_resume(resume_id):
    # Fetch the resume by ID and ensure it belongs to the current user
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("You don't have permission to edit this resume.", 'danger')
        return redirect(url_for('resume.view_resumes'))

    form = ResumeForm(obj=resume)
    if form.validate_on_submit():
        # Update resume details
        resume.name = form.name.data
        resume.content = form.content.data
        db.session.commit()
        
        flash('Resume updated successfully!', 'success')
        return redirect(url_for('resume.view_resumes'))

    return render_template('edit_resume.html', form=form, resume=resume)

@bp.route('/delete_resume/<int:resume_id>', methods=['POST'])
@login_required
def delete_resume(resume_id):
    # Fetch the resume by ID and ensure it belongs to the current user
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("You don't have permission to delete this resume.", 'danger')
        return redirect(url_for('resume.view_resumes'))
    
    # Delete the resume
    db.session.delete(resume)
    db.session.commit()
    
    flash('Resume deleted successfully.', 'info')
    return redirect(url_for('resume.view_resumes'))

@bp.route('/generate_suggestions/<int:resume_id>', methods=['POST'])
@login_required
def generate_suggestions(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    suggestions = suggest_improvements(resume.content)
    flash(suggestions, 'info')  # Flash the suggestions to the user
    return redirect(url_for('resume.view_resumes'))  # Redirect to view resumes

@bp.route('/view_resume/<int:resume_id>')
@login_required
def view_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("You don't have permission to view this resume.", 'danger')
        return redirect(url_for('resume.view_resumes'))
    
    template = Template.query.get(resume.template_name)
    return render_template(f'resume_templates/{template.name}.html', resume=resume)
