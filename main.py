from flask import Flask,request
from  models import  init_db,DATA,get_all_books,add_books,add_bookings

app = Flask(__name__)

@app.route('/room/')
def all_books():
    chek_in=str(request.args.get('checkIn'))
    chek_out = str(request.args.get('checkOut'))
    guestsnum = int(request.args.get('guestsNum'))
    books = get_all_books(chek_in,chek_out,guestsnum)


    dict={'id':{}}
    for i in books:
        dict['id'][i['id']]={'floor':i['floor'],'guestsnum':i['guestsnum'],'beds':i['beds'],'price':i['price']}
    print(dict)

    return dict

@app.route('/add-room',methods=["POST","GET"])
def add_room():
    if request.method=='POST':
        floor=int(request.json['floor'])
        beds = int(request.json['beds'])
        guestsnum = int(request.json['guestNum'])
        price=int(request.json['price'])
        books = add_books(floor,guestsnum,beds,price)


        return books

@app.route('/booking',methods=["POST","GET"])
def add_booking():
    if request.method=='POST':
        chek_in=str(request.json['bookingDates']['checkIn'])
        chek_out = str(request.json['bookingDates']['checkOut'])
        firstname= str(request.json['firstName'])
        lasttname= str(request.json['lastName'])
        room_id = int(request.json['roomId'])
        books = add_bookings(firstname,lasttname,chek_in,chek_out,room_id)
        return books







if __name__ == '__main__':
    init_db(DATA)


    app.run(debug=True)