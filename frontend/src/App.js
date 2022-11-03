import {useEffect, useState} from 'react';
import axios from 'axios';
import {format} from "date-fns"
import './App.css';

const baseUrl = "http://127.0.0.1:5000";

function App() {
  const [description, setDescription] = useState("");
  const [eventsList, setEventsList] = useState([]);
  const [eventID, setEventID] = useState(null);
  const [editDescription, setEditDescription] = useState("");

  const fetchEvents = async () => {
    const data = await axios.get(`${baseUrl}/events`);
    const { events } = data.data;
    setEventsList(events);
  }

  const handleChange = e => {
    setDescription(e.target.value);
  }

  const handleDelete = async (id) => {
    try{
      await axios.delete(`${baseUrl}/events/${id}`);
      // const updatedList = eventsList.filter(event => event.id !== id);
      // setEventsList(updatedList);
      fetchEvents();
    }catch(err){
      console.log(err.message);
    }
  }
  const handleEdit = (event) => {
    setEventID(event.id);
    setEditDescription(event.description);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try{
      const data = await axios.post(`${baseUrl}/events`, { description });
      setEventsList([...eventsList, data.data]);
      setDescription("");
    }catch (err) {
      console.error(err.message);
    }
  }

  useEffect(() => {
    fetchEvents();
  }, []);

  return (
    <div className="App">
      <header className="App-header" >
        <section>
          <form onSubmit={handleSubmit}>
              <label htmlFor="description">Description</label>
              <input
                type="text"
                name="description"
                id="description"
                value={description}
                onChange={handleChange}
                placeholder="Enter description"
              />
              <button type="submit">Submit</button>
            </form>
        </section>
        <section>
          <ul>
            {eventsList.map(event => (
              <li style={{display:"flex"}} key={event.id}>
                {format(new Date(event.created_at), "MM/dd HH:mm: ")}
                {event.description}
                <button type="button" onClick={() => handleDelete(event.id)}>X</button>
              </li>
            ))}
          </ul>
        </section>
      </header>
    </div>
  );
}

export default App;
