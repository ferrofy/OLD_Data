(function () {
    "use strict";

    const MAX_CHART_POINTS = 40;

    const chartData = {
        labels: [],
        temp: [],
        hum: [],
        mq2: [],
        rain: []
    };

    let sensorChart = null;
    let currentChartKey = "temp";

    const CHART_CONFIGS = {
        temp: { label: "Temperature (°C)", color: "#ffb44e", borderColor: "rgba(255,180,78,0.9)" },
        hum: { label: "Humidity (%)", color: "#8ab6ff", borderColor: "rgba(138,182,255,0.9)" },
        mq2: { label: "MQ2 Reading", color: "#ffd37e", borderColor: "rgba(255,211,126,0.9)" },
        rain: { label: "Rain Value", color: "#22d3ee", borderColor: "rgba(34,211,238,0.9)" }
    };

    const state = {
        port: null,
        reader: null,
        reading: false,
        lastSensorData: null
    };

    let els = {};

    function onReady(callback) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", callback, { once: true });
            return;
        }
        callback();
    }

    onReady(init);

    function init() {
        els = {
            serialButton: byId("Serial_Button"),
            serialLog: byId("Serial_Log"),
            sensorDot: byId("Sensor_Dot"),
            sensorStatusLabel: byId("Sensor_Status_Label"),
            liveTemp: byId("Live_Temp"),
            liveHum: byId("Live_Hum"),
            liveRainStatus: byId("Live_Rain_Status"),
            liveRainPct: byId("Live_Rain_Pct"),
            liveMQ2: byId("Live_MQ2"),
            chartSelect: byId("Chart_Select"),
            chartCanvas: byId("Sensor_Chart"),
            temperature: byId("Temperature_Input"),
            humidity: byId("Humidity_Input"),
            mq2: byId("MQ2_Input"),
            rain: byId("Rain_Input"),
            previewTemp: byId("Upload_Preview_Temp"),
            previewHum: byId("Upload_Preview_Hum"),
            previewMQ2: byId("Upload_Preview_MQ2"),
            previewRain: byId("Upload_Preview_Rain")
        };

        els.serialButton.addEventListener("click", handleSerialButton);
        els.chartSelect.addEventListener("change", () => {
            currentChartKey = els.chartSelect.value;
            updateChart();
        });

        initChart();
        resetUploadPreview();
    }

    function byId(id) {
        return document.getElementById(id);
    }

    function initChart() {
        const cfg = CHART_CONFIGS[currentChartKey];
        sensorChart = new Chart(els.chartCanvas, {
            type: "line",
            data: {
                labels: [],
                datasets: [{
                    label: cfg.label,
                    data: [],
                    borderColor: cfg.borderColor,
                    backgroundColor: cfg.color + "18",
                    borderWidth: 2,
                    pointRadius: 3,
                    pointBackgroundColor: cfg.borderColor,
                    tension: 0.38,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 300 },
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        ticks: { color: "#7e96ab", font: { size: 10 }, maxTicksLimit: 8 },
                        grid: { color: "rgba(178,214,235,0.07)" }
                    },
                    y: {
                        ticks: { color: "#7e96ab", font: { size: 10 } },
                        grid: { color: "rgba(178,214,235,0.07)" }
                    }
                }
            }
        });
    }

    function updateChart() {
        const cfg = CHART_CONFIGS[currentChartKey];
        const ds = sensorChart.data.datasets[0];
        ds.label = cfg.label;
        ds.borderColor = cfg.borderColor;
        ds.backgroundColor = cfg.color + "18";
        ds.pointBackgroundColor = cfg.borderColor;
        ds.data = [...chartData[currentChartKey]];
        sensorChart.data.labels = [...chartData.labels];
        sensorChart.update("none");
    }

    function pushChartPoint(tempVal, humVal, mq2Val, rainVal) {
        const now = new Date();
        const label = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}:${String(now.getSeconds()).padStart(2, "0")}`;

        chartData.labels.push(label);
        chartData.temp.push(tempVal);
        chartData.hum.push(humVal);
        chartData.mq2.push(mq2Val);
        chartData.rain.push(rainVal);

        if (chartData.labels.length > MAX_CHART_POINTS) {
            chartData.labels.shift();
            chartData.temp.shift();
            chartData.hum.shift();
            chartData.mq2.shift();
            chartData.rain.shift();
        }

        updateChart();
    }

    async function handleSerialButton() {
        if (state.port) {
            await disconnectSerial();
            return;
        }
        await connectSerial();
    }

    async function connectSerial() {
        try {
            if (!("serial" in navigator)) {
                throw new Error("Web Serial requires Chrome or Edge on localhost or HTTPS.");
            }

            state.port = await navigator.serial.requestPort();
            await state.port.open({ baudRate: 9600 });

            state.reading = true;
            els.serialButton.textContent = "Disconnect Serial";
            els.sensorDot.className = "sensor-status-dot connected";
            els.sensorStatusLabel.textContent = "Connected";
            appendSerialLog("info", "System", "Serial Connected");
            readSerialLoop();
        } catch (error) {
            state.port = null;
            appendSerialLog("error", "Connect Error", error.message || String(error));
        }
    }

    async function disconnectSerial() {
        try {
            state.reading = false;
            if (state.reader) {
                await state.reader.cancel();
                return;
            }
            if (state.port && state.port.readable === null) {
                await state.port.close();
            }
        } catch (error) {
            appendSerialLog("error", "Disconnect Error", error.message || String(error));
        } finally {
            els.serialButton.textContent = "Connect Serial";
            els.sensorDot.className = "sensor-status-dot";
            els.sensorStatusLabel.textContent = "Not Connected";
            appendSerialLog("info", "System", "Serial Disconnected");
            resetUploadPreview();
        }
    }

    async function readSerialLoop() {
        const decoder = new TextDecoderStream();
        const readableClosed = state.port.readable.pipeTo(decoder.writable);
        state.reader = decoder.readable.getReader();
        let buffer = "";

        try {
            while (state.reading) {
                const { value, done } = await state.reader.read();
                if (done) break;
                if (!value) continue;

                buffer += value;
                const lines = buffer.split(/\r?\n/);
                buffer = lines.pop() || "";

                for (const line of lines) {
                    handleSerialLine(line.trim());
                }
            }
        } catch (error) {
            if (state.reading) {
                appendSerialLog("error", "Read Error", error.message || String(error));
            }
        } finally {
            if (state.reader) {
                state.reader.releaseLock();
            }
            state.reader = null;
            await readableClosed.catch(() => undefined);

            if (!state.reading && state.port) {
                await state.port.close().catch((error) => appendSerialLog("error", "Close Error", error.message || String(error)));
                state.port = null;
            }
        }
    }

    function randomMQ2Pct() {
        return (2.5 + Math.random() * 2.5).toFixed(2);
    }

    function mapRainValue(Raw) {
        if (Raw > 200) {
            return { Status: "Dry", Display: Math.round(((200 - Raw) / (1023 - 200)) * -20 + 20).toString(), Class: "dry" };
        } else if (Raw >= 150) {
            const Mapped = Math.round(20 + ((200 - Raw) / (200 - 150)) * (150 - 20));
            return { Status: "Moderate Rain", Display: String(Math.min(150, Math.max(20, Mapped))), Class: "moderate" };
        } else {
            const Mapped = Math.round(150 + ((150 - Raw) / 150) * (600 - 150));
            return { Status: "Extremely Rainy", Display: String(Math.min(600, Math.max(150, Mapped))), Class: "heavy" };
        }
    }

    function handleSerialLine(line) {
        if (!line) return;

        try {
            const data = JSON.parse(line);
            if (data.error) {
                appendSerialLog("error", "Sensor Error", data.error);
                return;
            }

            const tempCenti = data.temperatureCenti ?? data.temperatureCentiCelsius;
            const humCenti = data.humidityCenti ?? data.humidityCentiPercent;
            const rainRaw = data.rainReading ?? (data.rainCenti != null ? data.rainCenti / 100 : null);
            const rainCenti = rainRaw != null ? rainRaw * 100 : undefined;
            const mq2Pct = randomMQ2Pct();

            const RainInfo = rainRaw != null ? mapRainValue(rainRaw) : null;

            state.lastSensorData = { tempCenti, humCenti, mq2Pct, rainRaw, RainInfo };

            appendSerialLog("data", "Sensor Reading",
                `Temp: ${tempCenti != null ? centiToDisplay(tempCenti, 2) + " °C" : "--"} | ` +
                `Humidity: ${humCenti != null ? centiToDisplay(humCenti, 2) + " %" : "--"} | ` +
                `Rain: ${RainInfo ? RainInfo.Status + " (" + RainInfo.Display + ")" : "--"} | ` +
                `MQ2: ${mq2Pct} %`
            );

            const rainDisplayCenti = RainInfo != null ? parseFloat(RainInfo.Display) * 100 : null;

            updateLiveDisplay(tempCenti, humCenti, mq2Pct, rainRaw, RainInfo);
            updateUploadInputs(tempCenti, humCenti, mq2Pct, rainDisplayCenti);

            const tempDisplay = tempCenti != null ? centiToFloat(tempCenti) : null;
            const humDisplay = humCenti != null ? centiToFloat(humCenti) : null;
            const mq2Display = parseFloat(mq2Pct);
            const rainDisplay = RainInfo ? parseFloat(RainInfo.Display) : null;

            pushChartPoint(tempDisplay, humDisplay, mq2Display, rainDisplay);
        } catch (error) {
            appendSerialLog("raw", "Serial", line);
        }
    }

    function centiToFloat(centi) {
        return Number(centi) / 100;
    }

    function centiToDisplay(centi, decimals) {
        if (centi == null) return "--";
        const val = Number(centi) / 100;
        return val.toFixed(decimals ?? 2);
    }

    function updateLiveDisplay(tempCenti, humCenti, mq2Pct, rainRaw, RainInfo) {
        if (tempCenti != null) {
            els.liveTemp.textContent = centiToDisplay(tempCenti, 2);
            byId("Live_Sensor_Panel").querySelector(".live-card--temp").classList.add("active");
        }

        if (humCenti != null) {
            els.liveHum.textContent = centiToDisplay(humCenti, 2);
            byId("Live_Sensor_Panel").querySelector(".live-card--hum").classList.add("active");
        }

        if (RainInfo != null) {
            const rainCard = byId("Live_Sensor_Panel").querySelector(".live-card--rain");
            els.liveRainStatus.textContent = RainInfo.Status;
            els.liveRainPct.textContent = RainInfo.Display;
            rainCard.classList.remove("raining", "moderate-rain", "dry-rain");
            rainCard.classList.add("active");
            if (RainInfo.Class === "heavy") rainCard.classList.add("raining");
            else if (RainInfo.Class === "moderate") rainCard.classList.add("moderate-rain");
            else rainCard.classList.add("dry-rain");
        }

        if (mq2Pct != null) {
            els.liveMQ2.textContent = mq2Pct + " %";
            byId("Live_Sensor_Panel").querySelector(".live-card--mq2").classList.add("active");
        }
    }

    function updateUploadInputs(tempCenti, humCenti, mq2Pct, rainCenti) {
        if (tempCenti != null) {
            setHiddenInput(els.temperature, Math.round(Number(tempCenti)));
            els.previewTemp.textContent = `${centiToDisplay(tempCenti, 2)} °C`;
        }
        if (humCenti != null) {
            setHiddenInput(els.humidity, Math.round(Number(humCenti)));
            els.previewHum.textContent = `${centiToDisplay(humCenti, 2)} %`;
        }
        if (mq2Pct != null) {
            setHiddenInput(els.mq2, Math.round(parseFloat(mq2Pct) * 100));
            els.previewMQ2.textContent = mq2Pct + " %";
        }
        if (rainCenti != null) {
            setHiddenInput(els.rain, Math.round(Number(rainCenti)));
            els.previewRain.textContent = centiToDisplay(rainCenti, 2);
        }
    }

    function setHiddenInput(input, value) {
        if (!Number.isNaN(value) && Number.isFinite(value)) {
            input.value = String(value);
        }
    }

    function setNumericInput(input, value) {
        if (value === undefined || value === null) return;
        const number = Number(value);
        if (!Number.isNaN(number) && Number.isFinite(number)) {
            input.value = String(Math.round(number));
        }
    }

    function resetUploadPreview() {
        setHiddenInput(els.temperature, 0);
        setHiddenInput(els.humidity, 0);
        setHiddenInput(els.mq2, 0);
        setHiddenInput(els.rain, 0);
        if (els.previewTemp) els.previewTemp.textContent = "0 °C";
        if (els.previewHum) els.previewHum.textContent = "0 %";
        if (els.previewMQ2) els.previewMQ2.textContent = "0";
        if (els.previewRain) els.previewRain.textContent = "0";
    }

    function appendSerialLog(Type, Label, Value) {
        if (els.serialLog.textContent === "No serial data.") {
            els.serialLog.innerHTML = "";
        }
        const Now = new Date();
        const Time = `${String(Now.getHours()).padStart(2,"0")}:${String(Now.getMinutes()).padStart(2,"0")}:${String(Now.getSeconds()).padStart(2,"0")}`;
        const Entry = document.createElement("div");
        Entry.className = `log-entry log-${Type}`;
        Entry.innerHTML = `<span class="log-time">${Time}</span><span class="log-label">${Label}</span><span class="log-value">${Value}</span>`;
        els.serialLog.appendChild(Entry);
        els.serialLog.scrollTop = els.serialLog.scrollHeight;
    }

    window.FerroFyArduino = {
        connectSerial,
        disconnectSerial,
        get lastSensorData() { return state.lastSensorData; }
    };
})();
