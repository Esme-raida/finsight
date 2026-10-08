export default function Slider({ label, displayValue, min, max, step, value, onChange }) {
    return (
        <div className="slider-1">
            <div className="slider-label">
                <label>{label}</label>
                <span className="display-value">{displayValue}</span>
            </div>
            <input type="range" min={min} max={max} step={step} value={value} onChange={onChange} />
        </div>
    )
}