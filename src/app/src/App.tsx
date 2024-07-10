import './view/style/global.scss';
import { useState } from 'react';
import Shift from './view/components/Shift'

function App() {
  const [addshift, SetAddShift] = useState(false);

  function handleClick() {

    SetAddShift(!addshift);



  }



  return (
    <div className='wrapper'>

      <h1 className='header'>wellcome Bahal habait</h1>


      <button className='button' onClick={handleClick}>Add Shift</button>

      {addshift == true ? <Shift /> : <div></div>}





    </div>
  )
}

export default App
