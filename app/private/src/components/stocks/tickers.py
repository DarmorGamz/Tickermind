from fastapi import HTTPException
import json
import os
import string
from common.database import Database

class tickers:
    def __init__(self):
        pass

    async def Gsad(self, cmd: string, varsIn: dict = None) -> dict | None:
        match cmd:
            case "Get":
                raise HTTPException(400, "Invalid Cmd")
            case "GetList":
                # Initialize Database
                db = Database("../data/stocks.db", primary_table="stocks", secondary_table="stock_data", news_table="news_table", foreign_key="stock_id")
                
                # Query to get all tickers, latest close price, and latest sentiment label
                query = """
                    SELECT s.ticker, sd.close, (
                        SELECT n.sentiment_label
                        FROM {news_table} n
                        WHERE n.{foreign_key} = s.id
                        ORDER BY n.date DESC
                        LIMIT 1
                    ) as sentiment_label
                    FROM {primary_table} s
                    LEFT JOIN {secondary_table} sd ON s.id = sd.{foreign_key}
                    WHERE sd.date = (
                        SELECT MAX(date)
                        FROM {secondary_table}
                        WHERE {foreign_key} = s.id
                    )
                """
                results = await db.fetch_all(query)

                # Format results as array of objects with explicit keys
                result_array = [
                    {
                        "ticker": row["ticker"],
                        "Close": row["close"],
                        "Sentiment_Label": row["sentiment_label"] if row["sentiment_label"] else "N/A"
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