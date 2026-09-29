"""add rag knowledge tables

Revision ID: d799c0d374b9
Revises: 18548e63f928
Create Date: 2026-09-29 06:37:24.682634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import VECTOR


# revision identifiers, used by Alembic.
revision: str = 'd799c0d374b9'
down_revision: Union[str, Sequence[str], None] = '18548e63f928'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute(
        "CREATE EXTENSION IF NOT EXISTS vector"
    )

    op.create_table(
        "knowledge_documents",

        sa.Column(
            "id",
            sa.Uuid(),
            nullable=False,
        ),

        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "source",
            sa.String(length=500),
            nullable=False,
        ),

        sa.Column(
            "content_hash",
            sa.String(length=64),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint("source"),
    )


    op.create_table(
        "document_chunks",

        sa.Column(
            "id",
            sa.BigInteger(),
            autoincrement=True,
            nullable=False,
        ),

        sa.Column(
            "document_id",
            sa.Uuid(),
            nullable=False,
        ),

        sa.Column(
            "chunk_index",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "embedding",
            VECTOR(dim=768),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["document_id"],
            ["knowledge_documents.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint(
            "document_id",
            "chunk_index",
            name="uq_document_chunk",
        ),
    )


    op.create_index(
        "ix_document_chunks_document_id",
        "document_chunks",
        ["document_id"],
        unique=False,
    )


def downgrade() -> None:

    op.drop_index(
        "ix_document_chunks_document_id",
        table_name="document_chunks",
    )

    op.drop_table(
        "document_chunks"
    )

    op.drop_table(
        "knowledge_documents"
    )