"""init schema

Revision ID: 20260207_0001
Revises: 
Create Date: 2026-02-07 18:40:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260207_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_roles = postgresql.ENUM(
        "member",
        "lead",
        "admin",
        name="user_roles",
        create_type=False,
    )
    attendance_status = postgresql.ENUM(
        "present",
        "absent",
        "excused",
        name="attendance_status",
        create_type=False,
    )
    op.execute(
        "DO $$ BEGIN CREATE TYPE user_roles AS ENUM ('member', 'lead', 'admin'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )
    op.execute(
        "DO $$ BEGIN CREATE TYPE attendance_status AS ENUM ('present', 'absent', 'excused'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_roles, nullable=False, server_default="member"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "classes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], name=op.f("fk_classes_created_by_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_classes")),
    )
    op.create_index(op.f("ix_classes_title"), "classes", ["title"], unique=False)

    op.create_table(
        "announcements",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
            name=op.f("fk_announcements_created_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_announcements")),
    )

    op.create_table(
        "qna_questions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], name=op.f("fk_qna_questions_author_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_qna_questions")),
    )
    op.create_index(op.f("ix_qna_questions_author_id"), "qna_questions", ["author_id"], unique=False)

    op.create_table(
        "quarterly_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quarter", sa.String(length=20), nullable=False),
        sa.Column("objectives", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
            name=op.f("fk_quarterly_plans_created_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_quarterly_plans")),
    )
    op.create_index(op.f("ix_quarterly_plans_quarter"), "quarterly_plans", ["quarter"], unique=False)

    op.create_table(
        "sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("starts_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], name=op.f("fk_sessions_class_id_classes")),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], name=op.f("fk_sessions_created_by_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sessions")),
    )
    op.create_index(op.f("ix_sessions_class_id"), "sessions", ["class_id"], unique=False)

    op.create_table(
        "enrollments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], name=op.f("fk_enrollments_class_id_classes")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_enrollments_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_enrollments")),
        sa.UniqueConstraint("user_id", "class_id", name=op.f("uq_enrollments_user_class")),
    )
    op.create_index(op.f("ix_enrollments_class_id"), "enrollments", ["class_id"], unique=False)
    op.create_index(op.f("ix_enrollments_user_id"), "enrollments", ["user_id"], unique=False)

    op.create_table(
        "qna_replies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("question_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], name=op.f("fk_qna_replies_author_id_users")),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["qna_questions.id"],
            name=op.f("fk_qna_replies_question_id_qna_questions"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_qna_replies")),
    )
    op.create_index(op.f("ix_qna_replies_question_id"), "qna_replies", ["question_id"], unique=False)

    op.create_table(
        "attendance",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("marked_by_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", attendance_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["marked_by_id"], ["users.id"], name=op.f("fk_attendance_marked_by_id_users")),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], name=op.f("fk_attendance_session_id_sessions")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_attendance_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_attendance")),
        sa.UniqueConstraint("session_id", "user_id", name=op.f("uq_attendance_session_user")),
    )
    op.create_index(op.f("ix_attendance_session_id"), "attendance", ["session_id"], unique=False)
    op.create_index(op.f("ix_attendance_user_id"), "attendance", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_attendance_user_id"), table_name="attendance")
    op.drop_index(op.f("ix_attendance_session_id"), table_name="attendance")
    op.drop_table("attendance")

    op.drop_index(op.f("ix_qna_replies_question_id"), table_name="qna_replies")
    op.drop_table("qna_replies")

    op.drop_index(op.f("ix_enrollments_user_id"), table_name="enrollments")
    op.drop_index(op.f("ix_enrollments_class_id"), table_name="enrollments")
    op.drop_table("enrollments")

    op.drop_index(op.f("ix_sessions_class_id"), table_name="sessions")
    op.drop_table("sessions")

    op.drop_index(op.f("ix_quarterly_plans_quarter"), table_name="quarterly_plans")
    op.drop_table("quarterly_plans")

    op.drop_index(op.f("ix_qna_questions_author_id"), table_name="qna_questions")
    op.drop_table("qna_questions")

    op.drop_table("announcements")

    op.drop_index(op.f("ix_classes_title"), table_name="classes")
    op.drop_table("classes")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    op.execute("DROP TYPE IF EXISTS attendance_status")
    op.execute("DROP TYPE IF EXISTS user_roles")
