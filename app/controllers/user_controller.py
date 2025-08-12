from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List
from datetime import datetime
from app.schemas.user import UserBase , UserCreate,UserResponse,UserRole,UserUpdate
from fastapi import HTTPException
from passlib.hash import bcrypt
from db_init import get_db_connection




def create_user(user_data: UserCreate) -> UserResponse:
    conn = get_db_connection()
    cur = conn.cursor()

    hashed_password = bcrypt.hash(user_data.password)

    cur.execute("""
        INSERT INTO users (name, email, password_hash, role, department_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, name, email, role, department_id, created_at;
    """, (
        user_data.name,
        user_data.email,
        hashed_password,
        user_data.role,
        user_data.department_id
    ))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return UserResponse(
        id=row[0], name=row[1], email=row[2], role=row[3],
        department_id=row[4], created_at=row[5]
    )


def get_users() -> List[UserResponse]:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, role, department_id, created_at
        FROM users
        ORDER BY created_at DESC;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        UserResponse(
            id=r[0], name=r[1], email=r[2], role=r[3],
            department_id=r[4], created_at=r[5]
        )
        for r in rows
    ]


def get_user_by_id(user_id: int) -> UserResponse:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, role, department_id, created_at
        FROM users
        WHERE id = %s;
    """, (user_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=row[0], name=row[1], email=row[2], role=row[3],
        department_id=row[4], created_at=row[5]
    )


def update_user(user_id: int, update_data: UserUpdate) -> UserResponse:
    conn = get_db_connection()
    cur = conn.cursor()

    if update_data.password:
        hashed_password = bcrypt.hash(update_data.password)
        cur.execute("""
            UPDATE users
            SET name = %s, email = %s, password_hash = %s, role = %s, department_id = %s
            WHERE id = %s
            RETURNING id, name, email, role, department_id, created_at;
        """, (
            update_data.name,
            update_data.email,
            hashed_password,
            update_data.role,
            update_data.department_id,
            user_id
        ))
    else:
        cur.execute("""
            UPDATE users
            SET name = %s, email = %s, role = %s, department_id = %s
            WHERE id = %s
            RETURNING id, name, email, role, department_id, created_at;
        """, (
            update_data.name,
            update_data.email,
            update_data.role,
            update_data.department_id,
            user_id
        ))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=row[0], name=row[1], email=row[2], role=row[3],
        department_id=row[4], created_at=row[5]
    )


def delete_user(user_id: int) -> dict:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM users
        WHERE id = %s
        RETURNING id;
    """, (user_id,))

    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User {deleted[0]} deleted successfully"}
