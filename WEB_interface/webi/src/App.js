import logo from './logo.svg';
import './App.css';
import TechMain from './TechnicianPage/TechnicianMain' 

function App() {

  const tasks = {
    "Task1" : 5,
    "Task2" : 7,
    "Task3" : 3,
    "Task4" : 9,
    "Task5" : 5,
    "Task6" : 5,
    "Task7" : 5,
    "Task8" : 1,
    "Task9" : 5,
    "Task10" : 10,
    "Task11" : 5,
  }

  const technicians = {
    "Tec1" : ["Task3","Task5","Task8","Task9" ],
    "Tec2" : ["Task1","Task2","Task4","Task6" ],
    "Tec3" : ["Task7","Task10","Task11" ]
  }

  const getInput = () => {
    return {"tasks" : tasks, "technicians" : technicians}
  }

  const getTasksTech = (name) => {
    const input = getInput()
    const tasksTech = input["technicians"][name]
    const res = []
    for (let task of tasksTech){
      const lengthTask = input["tasks"][task]
      res.push([task, lengthTask])
    }
    return res
  }

  const currentTech = "Tec1"

  return (
    <div className="App">
     <TechMain name={currentTech} listTasks={getTasksTech(currentTech)}  />
    </div>
  );
}

export default App;
