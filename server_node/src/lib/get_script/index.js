//import {PythonShell} from 'python-shell';
const {PythonShell} = require('python-shell')

module.exports = async function get_script(id){

let options = {
    mode: 'text',
    pythonPath: 'python',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: './src/lib/get_script', //'./src/lib/get_script',
    args: [id]
};


 const result = await new Promise((resolve, reject) => { PythonShell.run('get_script.py', options,  (err, results) => {
    if(err) reject(err);
    //console.log(results);
   
    return resolve(results);
    });
 });
    return result
}