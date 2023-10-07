import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

import './LandPage.scss';
export default function ManyTechsGraph({ input }) {

const { abs, min, max, round } = Math;
const moreCostlyTask = max(...Object.values(input["tasks"]))
    function generateRandomColor(){
    let maxVal = 0xFFFFFF; // 16777215
    let randomNumber = Math.random() * maxVal; 
    randomNumber = Math.floor(randomNumber);
    randomNumber = randomNumber.toString(16);
    let randColor = randomNumber.padStart(6, 0);   
    return `#${randColor.toUpperCase()}`
}

function numberToColorHsl(i) {
    // as the function expects a value between 0 and 1, and red = 0° and green = 120°
    // we convert the input to the appropriate hue value
    var hue = i * 1.2 / 360;
    // we convert hsl to rgb (saturation 100%, lightness 50%)
    var rgb = hslToRgb(hue, 1, .5);
    // we format to css value and return
    return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')'; 
}
function hslToRgb(h, s, l) {
  let r, g, b;

  if (s === 0) {
    r = g = b = l; // achromatic
  } else {
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hueToRgb(p, q, h + 1/3);
    g = hueToRgb(p, q, h);
    b = hueToRgb(p, q, h - 1/3);
  }

  return [round(r * 255), round(g * 255), round(b * 255)];
}

function hueToRgb(p, q, t) {
  if (t < 0) t += 1;
  if (t > 1) t -= 1;
  if (t < 1/6) return p + (q - p) * 6 * t;
  if (t < 1/2) return q;
  if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
  return p;
}


    const options = {
        indexAxis: 'y',
        scales: {
            x: {
                stacked: true,
            },

            y: {
                stacked: true,
            }
        },
        elements: {
            bar: {
                borderWidth: 2,
            },
        },
        responsive: true,
        plugins: {
            legend: {
                position: 'right',
            },
            title: {
                display: true,
                text: 'Tarefas por técnico',
            },
        },
    };

    const labels = Object.keys(input["technicians"])  //['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    const datasetsFromInput = () => {
        const res = []
        for (let [tecName, tasks] of Object.entries(input["technicians"])) {
            for (let task of tasks) {
                const cost = input["tasks"][task]
                const dataThisTask =  Array(labels.length).fill(0); 
                dataThisTask[labels.indexOf(tecName)] = cost
                res.push({
                    label: task, 
                    data: dataThisTask, 
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: numberToColorHsl((1-(cost / moreCostlyTask))*100),
                })
            }

        }
        return res
    }

    const data = {
        labels,
        datasets: datasetsFromInput()
    };




    return (
            <div className='tabelTecs'>
            <Bar options={options} data={data} />
    </div>
    )

}