const express = require('express');
const mongoose = require('mongoose');
const csvtojson = require('csvtojson');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(bodyParser.json());
app.use(cors());

mongoose.connect('mongodb://127.0.0.1:27017/flightOffers')
    .then(() => console.log('Connected to MongoDB'))
    .catch((err) => console.error('MongoDB connection error:', err));


const flightSchema = new mongoose.Schema({
    Departure: { type: String, required: true },
    Arrival: { type: String, required: true },
    Price: { type: Number, required: true },
    DepartureDate: { type: String, required: true },
    ArrivalDate: { type: String, required: true }
});
const Flight = mongoose.model('Flight', flightSchema);

app.post('/import', async (req, res) => {
    try {
        const filePath = path.join(__dirname, 'flight_offers.csv');
        const jsonArray = await csvtojson().fromFile(filePath);
        const formattedData = jsonArray.map(flight => ({
            Departure: flight.Departure,
            Arrival: flight.Arrival,
            Price: parseFloat(flight.Price),
            DepartureDate: flight['Departure Date'],
            ArrivalDate: flight['Arrival Date']
        })).filter(flight => flight.Departure && flight.Arrival && !isNaN(flight.Price));

        await Flight.insertMany(formattedData);
        res.json(formattedData); 
    } catch (err) {
        res.status(500).send('Error importing data: ' + err.message);
    }
});



app.get('/flights', async (req, res) => {
    const { page = 1, limit = 10, search = '' } = req.query;
    try {
        const query = search ? {
            $or: [
                { Departure: { $regex: search, $options: 'i' } },
                { Arrival: { $regex: search, $options: 'i' } },
                { Price: { $regex: search, $options: 'i' } },
            ]
        } : {};

        const flights = await Flight.find(query)
            .skip((page - 1) * limit)
            .limit(parseInt(limit));
        const total = await Flight.countDocuments(query);
        res.json({ total, flights });
    } catch (err) {
        res.status(500).send('Error fetching data: ' + err.message);
    }
});

app.post('/flights', async (req, res) => {
    const { Departure, Arrival, Price, DepartureDate, ArrivalDate } = req.body;
    try {
        const newFlight = new Flight({ Departure, Arrival, Price, DepartureDate, ArrivalDate });
        await newFlight.save();
        res.status(201).send('Flight created successfully!');
    } catch (err) {
        res.status(500).send('Error creating flight: ' + err.message);
    }
});

app.put('/flights/:id', async (req, res) => {
    const { id } = req.params;
    const { Departure, Arrival, Price, DepartureDate, ArrivalDate } = req.body;
    try {
        const updatedFlight = await Flight.findByIdAndUpdate(id, {
            Departure, Arrival, Price, DepartureDate, ArrivalDate
        }, { new: true });
        if (updatedFlight) {
            res.send('Flight updated successfully!');
        } else {
            res.status(404).send('Flight not found');
        }
    } catch (err) {
        res.status(500).send('Error updating flight: ' + err.message);
    }
});

app.delete('/flights/:id', async (req, res) => {
    const { id } = req.params;
    try {
        const deletedFlight = await Flight.findByIdAndDelete(id);
        if (deletedFlight) {
            res.send('Flight deleted successfully!');
        } else {
            res.status(404).send('Flight not found');
        }
    } catch (err) {
        res.status(500).send('Error deleting flight: ' + err.message);
    }
});

app.get('/bigdata/analysis', async (req, res) => {
    try {
        const avgPrice = await Flight.aggregate([
            { $group: { _id: null, avgPrice: { $avg: "$Price" } } }
        ]);
        res.json({ avgPrice: avgPrice[0]?.avgPrice || 0 });
    } catch (err) {
        res.status(500).send('Error in Big Data analysis: ' + err.message);
    }
});

const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));