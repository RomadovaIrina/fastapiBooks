from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from src.models.seller import Seller
from icecream import ic
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.configurations import get_async_session
from src.schemas.seller import ReturnedSeller, IncomingSeller,\
    ReturnedAllSellers


seller_router = APIRouter(tags=["seller"], prefix="/seller")


DBSession = Annotated[AsyncSession, Depends(get_async_session)]


# Ручка для создания записи о продавце в БД.
@seller_router.post("/", response_model=ReturnedSeller,
                    status_code=status.HTTP_201_CREATED)  
async def register_seller(
    seller_data: IncomingSeller,
    session: DBSession
):
    new_seller = Seller(
    first_name=seller_data.first_name,
    last_name=seller_data.last_name,
    e_mail=seller_data.e_mail,
    password=seller_data.password
    )

    session.add(new_seller)
    await session.flush()

    return new_seller


# Получаем всех пользователей
@seller_router.get("/", response_model = ReturnedAllSellers)
async def get_sellers(session: DBSession):
    query = select(Seller).options(selectinload(Seller.seller_books))
    result = await session.execute(query)
    sellers = result.scalars().all()
    ic(sellers)
    return {"sellers": sellers}


# Получаем одного пользователя
@seller_router.get("/{seller_id}", response_model=ReturnedSeller)
async def get_seller(seller_id: int, session: DBSession):
    if result := await session.get(Seller, seller_id):
        return result

    return Response(status_code=status.HTTP_404_NOT_FOUND)


# Обновляем дааные продавца
@seller_router.put("/{seller_id}",)
async def update_seller(book_id: int,session: DBSession):
    pass


# Удаляем продавца => еще и его книги
@seller_router.delete("/{seller_id}",)
async def delete_seller(seller_id: int, session: DBSession):
    deleted_seller = await session.get(Seller, seller_id)
    if not deleted_seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await session.delete(deleted_seller)
    await session.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

