import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
    const [flights, setFlights] = useState([]);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [total, setTotal] = useState(0);
    const [selectedFlight, setSelectedFlight] = useState(null);
    const [formData, setFormData] = useState({
        Departure: '',
        Arrival: '',
        Price: '',
        DepartureDate: '',
        ArrivalDate: ''
    });
    const limit = 10;

    const fetchFlights = () => {
        setLoading(true);
        axios
            .get(`http://localhost:5000/flights?page=${page}&limit=${limit}`)
            .then(response => {
                const data = response.data;
                setFlights(Array.isArray(data.flights) ? data.flights : []);
                setTotal(data.total || 0);
                setLoading(false);
            })
            .catch(err => {
                console.error('Error fetching data:', err);
                setError('Failed to fetch data. Please try again later.');
                setFlights([]);
                setLoading(false);
            });
    };

    useEffect(() => {
        fetchFlights();
    }, [page]);

    const handleImport = () => {
      axios.post('http://localhost:5000/import')
          .then(response => {
              setFlights(response.data);  
              alert('Data imported successfully!');
          })
          .catch(err => {
              console.error('Error importing data:', err);
              alert('Failed to import data.');
          });
  };
  
  

    const handleResetData = () => {
        if (window.confirm('Are you sure you want to reset the data?')) {
            axios.post('http://localhost:5000/reset')
                .then(() => {
                    alert('Data reset successfully!');
                    fetchFlights();
                })
                .catch(err => {
                    console.error('Error resetting data:', err);
                    alert('Failed to reset data.');
                });
        }
    };

    const handleSearchChange = (e) => {
        setSearch(e.target.value);
    };

    const handleFormChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({ ...prevState, [name]: value }));
    };

    const handleCreate = () => {
        axios.post('http://localhost:5000/flights', formData)
            .then(() => {
                alert('Flight created successfully!');
                fetchFlights();
                setFormData({ Departure: '', Arrival: '', Price: '', DepartureDate: '', ArrivalDate: '' });
            })
            .catch(err => {
                console.error('Error creating flight:', err);
                alert('Failed to create flight.');
            });
    };

    const handleUpdate = () => {
        axios.put(`http://localhost:5000/flights/${selectedFlight._id}`, formData)
            .then(() => {
                alert('Flight updated successfully!');
                fetchFlights();
                setSelectedFlight(null);
                setFormData({ Departure: '', Arrival: '', Price: '', DepartureDate: '', ArrivalDate: '' });
            })
            .catch(err => {
                console.error('Error updating flight:', err);
                alert('Failed to update flight.');
            });
    };

    const handleDelete = (id) => {
        if (window.confirm('Are you sure you want to delete this flight?')) {
            axios.delete(`http://localhost:5000/flights/${id}`)
                .then(() => {
                    alert('Flight deleted successfully!');
                    fetchFlights();
                })
                .catch(err => {
                    console.error('Error deleting flight:', err);
                    alert('Failed to delete flight.');
                });
        }
    };

    const handleEdit = (flight) => {
        setSelectedFlight(flight);
        setFormData({
            Departure: flight.Departure,
            Arrival: flight.Arrival,
            Price: flight.Price,
            DepartureDate: flight.DepartureDate,
            ArrivalDate: flight.ArrivalDate
        });
    };

    const filteredFlights = Array.isArray(flights)
        ? flights.filter(flight =>
            `${flight.Departure} ${flight.Arrival} ${flight.Price}`
                .toLowerCase()
                .includes(search.toLowerCase())
        )
        : [];

    return (
        <div className="app-container">
            <h1>Flight Offers</h1>
            <button className="import-btn" onClick={handleImport}>Import Data</button>
            <button className="reset-btn" onClick={handleResetData}>Reset Data</button>
            <input
                className="search-input"
                type="text"
                placeholder="Search flights..."
                value={search}
                onChange={handleSearchChange}
            />

            {loading && <p>Loading data...</p>}
            {error && <p className="error">{error}</p>}

            {!loading && !error && (
                <>
                    <table className="flight-table">
                        <thead>
                            <tr>
                                <th>Departure</th>
                                <th>Arrival</th>
                                <th>Price</th>
                                <th>Departure Date</th>
                                <th>Arrival Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredFlights.length > 0 ? (
                                filteredFlights.map((flight, index) => (
                                    <tr key={index}>
                                        <td>{flight.Departure}</td>
                                        <td>{flight.Arrival}</td>
                                        <td>{flight.Price}</td>
                                        <td>{flight.DepartureDate}</td>
                                        <td>{flight.ArrivalDate}</td>
                                        <td>
                                            <button className="edit-btn" onClick={() => handleEdit(flight)}>Edit</button>
                                            <button className="delete-btn" onClick={() => handleDelete(flight._id)}>Delete</button>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="6">No results found for your search.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>

                    <div className="pagination">
                        <button
                            onClick={() => setPage(prev => Math.max(prev - 1, 1))}
                            disabled={page === 1}
                            className="pagination-btn"
                        >
                            Previous
                        </button>
                        <span>Page {page}</span>
                        <button
                            onClick={() => setPage(prev => (page * limit < total ? prev + 1 : prev))}
                            disabled={page * limit >= total}
                            className="pagination-btn"
                        >
                            Next
                        </button>
                    </div>

                    <div className="flight-form">
                        <h2>{selectedFlight ? 'Edit Flight' : 'Add Flight'}</h2>
                        <input
                            type="text"
                            name="Departure"
                            value={formData.Departure}
                            onChange={handleFormChange}
                            placeholder="Departure"
                        />
                        <input
                            type="text"
                            name="Arrival"
                            value={formData.Arrival}
                            onChange={handleFormChange}
                            placeholder="Arrival"
                        />
                        <input
                            type="number"
                            name="Price"
                            value={formData.Price}
                            onChange={handleFormChange}
                            placeholder="Price"
                        />
                        <input
                            type="text"
                            name="DepartureDate"
                            value={formData.DepartureDate}
                            onChange={handleFormChange}
                            placeholder="Departure Date"
                        />
                        <input
                            type="text"
                            name="ArrivalDate"
                            value={formData.ArrivalDate}
                            onChange={handleFormChange}
                            placeholder="Arrival Date"
                        />
                        <button
                            className="submit-btn"
                            onClick={selectedFlight ? handleUpdate : handleCreate}
                        >
                            {selectedFlight ? 'Update Flight' : 'Add Flight'}
                        </button>
                    </div>
                </>
            )}
        </div>
    );
};

export default App;
