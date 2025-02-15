import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

phone_book = {}
app = FastAPI()

class PhoneEntry(BaseModel):
    name: str
    number: str

@app.post("/add")
def add_phone(entry: PhoneEntry):
    phone_book[entry.name] = entry.number
    return {"message": "Phone number added", "data": list(phone_book.items())}

@app.delete("/delete/{name}")
def delete_phone(name: str):
    if name in phone_book:
        del phone_book[name]
        return {"message": "Phone number deleted", "data": list(phone_book.items())}
    raise HTTPException(status_code=404, detail="Name not found")

@app.put("/update")
def update_phone(entry: PhoneEntry):
    if entry.name in phone_book:
        phone_book[entry.name] = entry.number
        return {"message": "Phone number updated", "data": list(phone_book.items())}
    raise HTTPException(status_code=404, detail="Name not found")

@app.get("/list")
def list_phone_numbers():
    return [{"name": name, "number": number} for name, number in phone_book.items()]

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=5000)
