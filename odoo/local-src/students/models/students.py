from odoo import fields, models


class StudentsTraining(models.Model):
    _name = "students.training"
    _description = "Training table"
    _rec_name = "code"

    code = fields.Char(string="Training code", size=4, required=True)
    name = fields.Char(string="Training name", size=100, required=True)
    student_ids = fields.One2many(
        string="Training students",
        comodel_name="students.student",
        inverse_name="training_id",
    )


class StudentsStudent(models.Model):
    _name = "students.student"
    _description = "Student table"
    _rec_name = "lastname"
    number = fields.Char("Student number", size=11, required=True)
    firstname = fields.Char("Student firstname", size=64, required=True)
    lastname = fields.Char("Student lastname", size=64, required=True)

    training_id = fields.Many2one(
        string="Training",
        comodel_name="students.training",
        ondelete="cascade",
    )

    mark_ids = fields.One2many(
        string="Mark students",
        comodel_name="students.mark",
        inverse_name="student_id",
    )


class StudentMark(models.Model):
    _name = "students.mark"
    _description = "Mark table"

    COEFFICIENT_SELECTION = [('1', '1'), ('2', '2'), ('3', '3'), ('5', '5')]

    coefficient = fields.Selection(
        COEFFICIENT_SELECTION,
        string='Coefficient',
        default='1',
        index=True,
        required=True,
        help='Select a coefficient in the list'
    )

    computed_note = fields.Float(
        string='Computed Note',
        compute='_compute_note'
    )

    def _compute_note(self):
        for record in self:
            record.computed_note = float(record.mark) * float(record.coefficient)

    subject = fields.Char("Mark subject", size=64, required=True)
    mark = fields.Integer("Mark Mark", required=True)
    student_id = fields.Many2one(
        string="Student",
        comodel_name="students.student",
        ondelete="cascade",
    )
