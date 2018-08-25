# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : drift.py
# @Software: PyCharm


 @web.route('/drift/<int:did>/reject')
 def reject_drift(did):
     pass
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的，不能向自己索要书籍！')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enought_beans.html', beans=current_user.beans)