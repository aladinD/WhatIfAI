<script>
import {
    Line
} from 'vue-chartjs'
import chartjsPluginAnnotation from './chartjs-plugin-annotation.js'
import Printable from '@/mixins/Printable'
export default {
    extends: Line,
    mixins: [Printable],
    props: {
        chartData: {
            type: Array,
            required: true

        },
        chartLabels: {
            type: Array,
            required: true
        },
        axisLabel:{
            type: String,
            required: true
        }
    },
    data() {
        return {
            gradient: null,
            options: {
                showScale: true,
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: this.axisLabel,
                            fontSize: 14
                        },
                        ticks: {
                            beginAtZero: false,
                            precision: 0,
                            callback: (value, index, values) => {
                                return this.formatNumber(value)
                            }
                        },
                        gridLines: {
                            display: true,
                            color: '#EEF0F4',
                            borderDash: [5, 15]
                        }
                    }],
                    xAxes: [{
                        gridLines: {
                            display: true,
                            color: '#EEF0F4',
                            borderDash: [5, 15]
                        }
                    }]
                },
                annotation: {
                    annotations: [{
                        type: "line",
                        mode: "vertical",
                        scaleID: "x-axis-0",
                        value: "2020-01-01",
                        borderColor: "#e53935",
                        borderWidth: 2,
                        borderDash:[10, 10],
                        label: {
                            content: "PREDICTION START",
                            enabled: true,
                            position: "top"
                        }
                    }]
                },

                responsive: true,
                maintainAspectRatio: false

            }
        }
    },

    mounted() {
        this.gradient = this.$refs.canvas
            .getContext('2d')
            .createLinearGradient(0, 0, 0, 450)
        this.gradient.addColorStop(0, 'rgba(52, 217, 221, 0.6)')
        this.gradient.addColorStop(0.5, 'rgba(52, 217, 221, 0.25)')
        this.gradient.addColorStop(1, 'rgba(52, 217, 221, 0)')

        this.$forceUpdate();
        this.addPlugin([chartjsPluginAnnotation]),
        this.renderChart({
            labels: this.chartLabels,
            datasets: this.chartData
        }, this.options)
        setTimeout(() => {
            this.download()
        }, 500)
    },

    methods: {
        formatNumber(num) {
            let numString = Math.round(num).toString()
            let numberFormatMapping = [
                [6, 'm'],
                [3, 'k']
            ]
            for (let [numberOfDigits, replacement] of numberFormatMapping) {
                if (numString.length > numberOfDigits) {
                    let decimal = ''
                    if (numString[numString.length - numberOfDigits] !== '0') {
                        decimal = '.' + numString[numString.length - numberOfDigits]
                    }
                    numString = numString.substr(0, numString.length - numberOfDigits) + decimal + replacement
                    break
                }
            }
            return numString
        }
    }
}
</script>
