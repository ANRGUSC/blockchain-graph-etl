import React, {useState, useEffect} from 'react'
import './App.css';


function App() {
  const [data, setData] = useState([{}])

  useEffect(() =>{
    fetch("/test").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])
  return (
    
    <div>
      <h1>hi</h1>
    </div>
  )
}

export default App
