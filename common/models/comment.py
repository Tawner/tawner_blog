from .base import Base, db
from flask import request


class Comment(Base):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, comment="评论内容")

    # 外键关联
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), comment="文章id")
    article = db.relationship("Article", foreign_keys=[article_id])
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), comment="用户id")
    user = db.relationship("User", foreign_keys=[user_id])
    theme_id = db.Column(db.Integer, db.ForeignKey("comment.id"), comment="主题id")
    theme = db.relationship("Comment", foreign_keys=[theme_id])
    reply_comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"), comment="回复的评论id")
    reply_comment = db.relationship("Comment", foreign_keys=[reply_comment_id])

    @property
    def sub_comment_all(self):
        return Comment.query.filter_by(theme_id=self.id, is_delete=0).order_by(Comment.id.desc()).all()

    @property
    def reply(self):
        return Comment.query.filter_by(reply_comment_id=self.id, is_delete=0).all()

    @property
    def sub_comment(self):
        return self.sub_comment_all[:3]

    def get_page(self, page=1, rows=10):
        total = len(self.sub_comment_all)
        pages = (total // rows) + 1 if total % rows else total // rows

        if page < 1: page = 1
        if page > pages: page = pages

        has_next = False if page == pages else True
        has_prev = False if page == 1 else False
        res = {
            "page": page,
            "pages": pages,
            "rows": rows,
            "total": total,
            "has_next": has_next,
            "has_prev": has_prev,
            "items": self.sub_comment_all[(page - 1) * rows: page * rows]
        }
        return res

    @property
    def more_sub_comment(self):
        return True if len(self.sub_comment_all) > 3 else False

    @classmethod
    def add(cls, content, article_id=None, reply_comment_id=None):
        data = {"user_id": request.current_user.id, "content": content}
        if reply_comment_id:
            reply_comment = Comment.query.filter_by(id=reply_comment_id, is_delete=0).first()
            data.update({
                "article_id": reply_comment.article_id,
                "theme_id": reply_comment.theme_id if reply_comment.theme_id else reply_comment.id,
                "reply_comment_id": reply_comment_id
            })
        elif article_id:
            data["article_id"] = article_id
        else:
            return {"status": "failure", "msg": "参数有误"}

        db.session.add(Comment(**data))
        db.session.commit()
        return {"status": "success", "msg": "评论成功"}

    def delete(self):
        Comment.query.filter_by(theme_id=self.id, is_delete=0).update({"is_delete": 1})
        super().delete()

