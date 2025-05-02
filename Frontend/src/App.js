import {useState, useEffect} from 'react'
import './App.css';
import './styles/main.css';

// import { getFromAPI, getHumanFromAPI, getPage} from './components/Helpers';
import { ComparePolygon, Polygon } from './components/DrawPolygon';
import { MUISearchComponent, MUIListComponent } from './components/Pagination';
import { Closest } from './components/Closest';

function Navigation( {setOption, setFirstAuthor, setSecondAuthor}) {
  return (
    <div className="navigation">
      <button onClick={() => {
        setOption(1);
        setFirstAuthor([]);
        setSecondAuthor([]);
        }} style={{ margin: "5px" }}>
        Search
      </button>
      <button onClick={() => {
        setOption(2);
        setFirstAuthor([]);
        setSecondAuthor([]);
      }
      } style={{ margin: "5px" }}>
        Compare
      </button>
    </div>
  )
}




function App() {
  const [option, setOption] = useState(1);
  const [firstAuthor, setFirstAuthor] = useState({});
  const [secondAuthor, setSecondAuthor] = useState({});

    return (
      <div style={{margin:'1%'}}>
      
      {
        option === 1 ? 
        <div className="main-container">
          <Navigation setOption={setOption} setFirstAuthor={setFirstAuthor} setSecondAuthor={setSecondAuthor} style={{textAlign: 'center'}}/>
          <div className='analytic-container'>
            <MUISearchComponent setFirstAuthor={setFirstAuthor} className="search-component" />
            <Polygon firstAuthor={firstAuthor} className="polygon" />
            <Closest className="closest" firstAuthor={firstAuthor} setOption={setOption} setFirstAuthor={setFirstAuthor} setSecondAuthor={setSecondAuthor} />
          </div>
        
        </div> 
        : 
        <div className="main-container">
          <Navigation setOption={setOption} setFirstAuthor={setFirstAuthor} setSecondAuthor={setSecondAuthor}  style={{textAlign: 'center'}}/>
          <div className='analytic-container'>
            <MUIListComponent setFirstAuthor={setFirstAuthor} setSecondAuthor={setSecondAuthor} className="list-component" />
            <ComparePolygon firstAuthor={firstAuthor} secondAuthor={secondAuthor} className="compare-polygon" />
            <div></div>
          </div>
        </div>
      }
      </div>
    );
  
}

export default App;
