from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class LibraryBookCategory(models.Model):
    _name = "library.book.category"
    _description = "Book Category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('Name', index=True, required=True)
    complete_name = fields.Char(compute='_compute_complete_name', recursive=True, store=True)
    parent_id = fields.Many2one('library.book.category', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True, )
    child_id = fields.One2many('library.book.category', 'parent_id', 'Child Categories')
    book_count = fields.Integer(compute='_compute_book_count', )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    def _compute_book_count(self):
        for obj in self:
            obj.product_count = self.env['library.book'].search_count([
                ('category_id', 'child', obj.id)
            ])

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    def stat_button(self):
        print('test')
