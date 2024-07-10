import axios from 'axios';


const Shift = () => {

    function handleShift(ev: any) {

        ev.preventDefault();
        console.log(ev.target.date.value);
        console.log(ev.target.employee[0].value);

        const body = {
            name:'yakov'
        }



        const result = axios.post('localhost:8000/createEvent', body );

    }







    return (
        <div className="shift">
            <form onSubmit={handleShift}>
                <div className="box">תאריך

                    <input type="date" name="date" />

                </div>

                <div className="box"> עובדים
                    <div className="box__wrapper">
                        <input type="checkbox" name="employee" value="Zohar" />
                        <label htmlFor="Zohar">Zohar</label>
                    </div>

                    <div className="box__wrapper">
                        <input type="checkbox" name="employee" value="Jenia" />
                        <label htmlFor="Jenia">Jenia</label>
                    </div>

                    <div className="box__wrapper">
                        <input type="checkbox" name="employee" value="Afik" />
                        <label htmlFor="Afik">Afik</label>
                    </div>

                    <div className="box__wrapper">
                        <input type="checkbox" name="employee" value="Roie" />
                        <label htmlFor="Roie">Roie</label>
                    </div>

                    <div className="box__wrapper">
                        <input type="checkbox" name="employee" value="Daniel" />
                        <label htmlFor="Daniel">Daniel</label>
                    </div>

                    <div className="box__wrapper">
                        <input type="checkbox" name="employee" value="Amit" />
                        <label htmlFor="Amit">Amit</label>
                    </div>

                </div>




                <div className="box">משמרת

                    <div className="box__wrapper">
                        <input type="checkbox" name="shift" value="Morning" />
                        <label htmlFor="Morning">Morning</label>
                    </div>

                    <div className="box__wrapper">
                        <input type="checkbox" name="shift" value="Night" />
                        <label htmlFor="Night">Night</label>
                    </div>

                </div>

                <input type="submit" value="Submit" />



            </form>
        </div>

    )




}

export default Shift