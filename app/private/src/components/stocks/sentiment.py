from fastapi import HTTPException
import json
import os
import string
from common.database import Database

class sentiment:
    def __init__(self):
        pass

    async def Gsad(self, cmd: str, varsIn: dict = None) -> dict | None:
        match cmd:
            case "Get":
                raise HTTPException(400, "Invalid Cmd")
            case "GetList":
                # Initialize Database
                db = Database("../data/stocks.db", primary_table="stocks", secondary_table="stock_data", news_table="news_table", foreign_key="stock_id")
                
                # Query to get all sentiment rows with ticker and all relevant fields
                query = """
                    SELECT s.ticker, n.sentiment_label, n.date, n.description, n.source
                    FROM {news_table} n
                    LEFT JOIN {primary_table} s ON n.{foreign_key} = s.id
                    ORDER BY n.date DESC
                """
                results = await db.fetch_all(query)

                # Format results as array of objects with explicit keys
                result_array = [
                    {
                        "ticker": row["ticker"],
                        "Sentiment_Label": row["sentiment_label"] if row["sentiment_label"] else "N/A",
                        "Date": row["date"],
                        "Description": row["description"] if row["description"] else "N/A",
                        "Source": row["source"]
                    }
                    for row in results
                ]

                # Return response with data key
                return {"data": result_array, "status": 200}
            case "Set":
                raise HTTPException(400, "Invalid Cmd")
            case "Add":
                raise HTTPException(400, "Invalid Cmd")
            case "Del":
                raise HTTPException(400, "Invalid Cmd")
            case "DelAll":
                raise HTTPException(400, "Invalid Cmd")
            case _:
                raise HTTPException(400, "Invalid Cmd")