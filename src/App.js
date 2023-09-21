import './App.css';
import Confirm from './Component/Confirm';
import DataTable from './Component/DataTable';
import NavHead from './Component/NavHead';
import New_Download from './Component/New_Download';
import Add_Url from './Component/Add_Url';
import Download_Progress from './Component/Download_Progress';

function App() {
  return (
    <div className="App" style={{border:"1px solid "}}>
      {/* <NavHead />
      <DataTable /> */}
      {/* <Confirm /> */}
      {/* <New_Download/> */}
      {/* <Add_Url /> */}
      <Download_Progress />
      
    </div>
  );
}


export default App;