from .base import Base, db


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
    theme = db.relationship("Comment", foreign_keys=[theme_id], backref="son_comment")
    reply_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), comment="回复对象")
    reply_user = db.relationship("User", foreign_keys=[reply_user_id])
