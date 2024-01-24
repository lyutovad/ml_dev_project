import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [surname, setSurname] = useState('');
  const [message, setMessage] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [modelsNames, setModelsNames] = useState([]);


  const handleRegister = async () => {
    try {
      const response = await axios.post(
        'http://localhost:9100/new_user',
        {
          username,
          password,
          email,
          name,
          surname,
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      setMessage(response.data.mes);
    } catch (error) {
      console.error('Error during registration:', error);
      setMessage('Error during registration');
    }
  };

  return response.json(); // parses JSON response into native JavaScript objects
}


return (
  <div>
    <h1>User Registration</h1>
    <label>Username:</label>
    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} /><br />

    <label>Password:</label>
    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /><br />

    <label>Email:</label>
    <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} /><br />

    <label>Name:</label>
    <input type="text" value={name} onChange={(e) => setName(e.target.value)} /><br />

    <label>Surname:</label>
    <input type="text" value={surname} onChange={(e) => setSurname(e.target.value)} /><br />

    <button onClick={handleRegister}>Register</button>

    {message && <p>{message}</p>}
  </div>
);

useEffect(() => {
  // Загрузка списка моделей при монтировании компонента
  async function fetchModelsNames() {
    try {
      const response = await axios.get('http://your-backend-url/models_names');
      setModelsNames(response.data);
    } catch (error) {
      console.error('Error fetching models names:', error);
    }
  }

  fetchModelsNames();
}, []); // Пустой массив зависимостей означает выполнение эффекта только при монтировании

const handleModelChange = (event) => {
  setSelectedModel(event.target.value);
};

const handleGetModelsNames = async () => {
  try {
    const response = await axios.get('http://your-backend-url/models_names');
    setModelsNames(response.data);
    setMessage('');
  } catch (error) {
    console.error('Error fetching models names:', error);
    setMessage('Error fetching models names');
  }
};

return (
  <div>
    <h1>Model Selection</h1>

    <label>Select a model:</label>
    <select value={selectedModel} onChange={handleModelChange}>
      <option value="">Select a model</option>
      {Object.entries(modelsNames).map(([key, value]) => (
        <option key={key} value={key}>
          {value}
        </option>
      ))}
    </select>

    <button onClick={handleGetModelsNames}>Get Models Names</button>

    {message && <p>{message}</p>}
  </div>
);


export default App;
