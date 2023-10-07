import ManyTechsGraph from "./ManyTechsGraph";

import './LandPage.scss';

export default function LandPage({ input }) {
    return (
        <div>
            <h1>Land page</h1>
            <div className="line">

                <ManyTechsGraph input={input} />;
                <div>
                    Botões
                </div>
            </div>
        </div>
    )
}