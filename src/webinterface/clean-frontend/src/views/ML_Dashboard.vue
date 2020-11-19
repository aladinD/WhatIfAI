<template>
<div class="wrapper">
    <div class="top-pinned">
        <notifications></notifications>
    </div>
    <parallax class="section page-header header-filter" :style="headerStyle"></parallax>
    <div class="main main-raised">
        <div class="section profile-content">

            <div class="container" id="faq">
            <h3 class="title no-margin">Getting started</h3>
                <div class="profile-tabs mx-auto tab-fix">
                    <tabs plain nav-pills-icons color-button="success">
                    </tabs>
                </div>
            </div>

            <div class="container" id="web">
                <h3 class="title">Web Traffic Analysis</h3>
                <div class="md-layout mx-auto fullwidth">
                    <div class="fsize-chart">
                        <div v-if="loading_graph1==true" class="loading-banner"><img type="image/svg+xml" src="@/assets/img/loading_graph.svg" /></div>
                        <line-chart v-if="loading_graph1 == false" ref="charty" :chartData="chartdata_graph1" :chartLabels="chartlabels_graph1" :axisLabel="dataset_axis_label" />
                    </div>
                    <!-- <div v-if="chartdata"> Predicted Class is: {{ chartdata }} yo {{ chartlabels }}</div> -->
                </div>
                <div class="md-layout mx-auto controls">
                    <md-menu md-size="medium" md-align-trigger class="menuu">
                        <md-button md-menu-trigger class="fixed-width-button">{{selectedDataset_graph1}}</md-button>
                        <md-menu-content>
                            <md-menu-item @click="dataset_id='0', selectedDataset_graph1='Internet Exchange Points', dataset_axis_label= 'bit/s'">Internet Exchange Points</md-menu-item>
                            <md-menu-item @click="dataset_id='1', selectedDataset_graph1='YouTube View Count', dataset_axis_label= 'Views per day'">YouTube View Count</md-menu-item> <!-- Was YouTube Viewchange-->
                            <md-menu-item @click="dataset_id='3', selectedDataset_graph1='Steam Network Users', dataset_axis_label= 'Users per day'">Steam Network Users</md-menu-item>
                            <md-menu-item @click="dataset_id='5', selectedDataset_graph1='Twitch View Count', dataset_axis_label= 'Views per day'">Twitch View Count</md-menu-item> <!-- Was Twitch Views -->
                            <md-menu-item @click="dataset_id='9', selectedDataset_graph1='PlayStation Network Users', dataset_axis_label= 'Users per day'">PlayStation Network Users</md-menu-item>
                        </md-menu-content>
                    </md-menu>
                    <md-button class="md-success md-round run" @click='select_set(1)'>Run Inference</md-button>
                </div>
                <p>
                </p>
            </div>

            <div class="code">
                <div v-if="selectedDataset_graph1=='Internet Exchange Points'">
                    <h4 class="title incode">Internet Exchange Points</h4>
                    In order to accurately depict the trend of an in- or decreasing internet traffic, 
                    data from worldwide exchange points are most representative and given in bitrates per time. <br />
                    <br>
                    These internet exchange points are the physical infrastructure nodes through which Internet Service Providers (ISPs) 
                    such as Deutsche Telekom or Vodafone as well as Content Delivery Networks (CDNs) exchange their internet traffic. As such, 
                    every package worldwide is sent through one of such exchange points. <br />
                    <br />
                    The selected Internet Exchange Points data set comprises international exchange nodes from Frankfurt, Hamburg, Munich, Duesseldorf, Moscow, London, Seattle, Nova Scotia
                    Helsinki, Glasgow and Cardiff.
                </div>
            
                <div v-else-if="selectedDataset_graph1=='YouTube View Count'"> <!-- Was YouTube Viewchange-->
                    <h4 class="title incode">YouTube View Count</h4>
                    YouTube - as one of the most popular content creator websites - has seen a surge in user activity during the pandemic. The website traffic has thus increased 
                    at a steady pace and can be described by the number of views. 
                    <br><br>
                    The selected YouTube View Count data set comprises the amount of views for the most popular channels on YouTube. The data was obtained by scraping through 
                    YouTube analytics using a custom build Youtube scraper.    
                </div>

                <div v-else-if="selectedDataset_graph1=='Steam Network Users'">
                    <h4 class="title incode">Steam Network Users</h4>
                    Online gaming has seen a surge during the COVID-19 pandemic on several platforms. <br />
                    <br />
                    The selected Steam Network Users data set describes the network activity (i.e. currently active users) 
                    on the Steam gaming platform for the respective timeline. 
                </div>

                <div v-else-if="selectedDataset_graph1=='Twitch View Count'"> <!-- Was Twitch Views -->
                    <h4 class="title incode">Twitch View Count</h4>
                    During the COVID-19 pandemic, online streaming has greatly increased.
                    The currently most popular (gaming) streaming platform Twitch has seen an 
                    increase in members as well as overall stream views. 
                    <br><br>
                    The selected Twitch View Count data set describes the amount of views for the
                    respective streams on the platform. The data was obtained by scraping
                    through Twitch analytics using a custom build Twitch scraper.
                </div>

                <div v-else-if="selectedDataset_graph1=='PlayStation Network Users'">
                    <h4 class="title incode">PlayStation Network Users</h4>
                    Online gaming has seen a significant surge in popularity during the COVID-19 pandemic on several
                    platforms.<br><br>
                    The selected PlayStation Network Users data set describes the network activity (i.e. currently active users) on Sony PlayStation consoles
                    for the respective timeline.
                </div>
                
                <div v-else>
                    <h4 class="title incode">No dataset selected yet</h4>
                </div>
            </div>

            <div class="container" id="stock">
                <h3 class="title">Economic Performance Analysis</h3>
                <div class="md-layout mx-auto fullwidth">
                    <div class="fsize-chart">
                        <div v-if="loading_graph2==true" class="loading-banner"><img type="image/svg+xml" src="@/assets/img/loading_graph.svg" /></div>
                        <line-chart v-if="loading_graph2 == false" ref="charty" :chartData="chartdata_graph2" :chartLabels="chartlabels_graph2" :axisLabel="''"/>
                    </div>
                    <!-- <div v-if="chartdata"> Predicted Class is: {{ chartdata }} yo {{ chartlabels }}</div> -->
                </div>
                <div class="md-layout mx-auto controls">
                    <md-menu md-size="medium" md-align-trigger class="menuu">
                        <md-button md-menu-trigger class="fixed-width-button">{{selectedDataset_graph2}}</md-button>
                        <md-menu-content>
                            <md-menu-item @click="dataset_id='10', selectedDataset_graph2='Medical Branch'">Medical Branch</md-menu-item> <!-- Was Medical Stock -->
                            <md-menu-item @click="dataset_id='11', selectedDataset_graph2='Banking Branch'">Banking Branch</md-menu-item> <!-- Was Banking Stock -->
                            <md-menu-item @click="dataset_id='12', selectedDataset_graph2='Energy Branch'">Energy Branch</md-menu-item> <!-- Was Energy Stock -->
                            <md-menu-item @click="dataset_id='13', selectedDataset_graph2='Oil Branch'">Oil Branch</md-menu-item> <!-- Was Oil Stock -->
                            <md-menu-item @click="dataset_id='14', selectedDataset_graph2='Steel Branch'">Steel Branch</md-menu-item> <!-- Was Steel Stock -->
                            <md-menu-item @click="dataset_id='15', selectedDataset_graph2='Automotive Branch'">Automotive Branch</md-menu-item> <!-- Was Automotive Stock -->
                            <md-menu-item @click="dataset_id='16', selectedDataset_graph2='Telecom Branch'">Telecom Branch</md-menu-item> <!-- Was Telecom Stock -->
                            <md-menu-item @click="dataset_id='17', selectedDataset_graph2='Tech Branch'">Tech Branch</md-menu-item> <!-- Was Tech Stock -->
                        </md-menu-content>
                    </md-menu>
                    <md-button class="md-success md-round run" @click='select_set(2)'>Run Inference</md-button>
                </div>

            </div>

            <div class="code">
                <div v-if="selectedDataset_graph2=='Medical Branch'"> <!-- Was Medical Stock -->
                    <h4 class="title incode">Medical Branch</h4>
                    <!-- The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br> -->

                    The selected Medical Branch data set comprises a feature set of the
                    currently most dominant medical tech companies. In particular, it contains stock market data from 16 companies such as <br><br>

                    (a) Evotec AG<br>
                    (b) Siemens Healthineers AG<br>
                    (c) BASF
                    <br><br>
                    and many others.
                </div>

                <div v-else-if="selectedDataset_graph2=='Banking Branch'"> <!-- Was Banking Stock -->
                    <h4 class="title incode">Banking Branch</h4>
                    <!-- The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br> -->

                    The selected Banking Branch data set comprises a feature set of the
                    currently most important financial institutions listed in the worldwide
                    stock indexes. In particular, it contains stock market data from 13 companies such as<br><br>

                    (a) Deutsche Bank<br>
                    (b) Goldman Sachs<br>
                    (c) JPMorgan Chase
                    <br><br>
                    and many others. 
                </div>

                <div v-else-if="selectedDataset_graph2=='Energy Branch'"> <!-- Was Energy Stock -->
                    <h4 class="title incode">Energy Branch</h4>
                    <!-- The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br> -->
                    
                    The selected Energy Branch data set comprises a feature set of the
                    currently most important companies with a focus in energy and electricity
                    operation listed in the worldwide stock indexes. In particular, it contains stock market data from 8 companies such as<br><br>

                    (a) Siemens AG<br>
                    (b) Duke Energy Corporation<br>
                    (c) Electricite de France SA
                    <br><br>
                    and many others.
                </div>

                <div v-else-if="selectedDataset_graph2=='Oil Branch'"> <!-- Was Oil Stock -->
                    <h4 class="title incode">Oil Branch</h4>
                    <!-- The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br> -->
                    
                    The selected Oil Branch data set comprises a feature set of the currently most important companies operating in the field of oil production.
                    In particular, it contains stock market data from 9 companies such as<br><br>

                    (a) Shell<br>
                    (b) ExxonMobil<br>
                    (c) ROSNEFT
                    <br><br>
                    and many others.
                </div>

                <div v-else-if="selectedDataset_graph2=='Steel Branch'"> <!-- Was Steel Stock -->
                    <h4 class="title incode">Steel Branch</h4>
                    <!-- The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br> -->
                    
                    The selected Steel Branch data set comprises a feature set of the currently most important companies operating in the field of steel production.
                    In particular, it contains stock market data from 7 companies such as<br><br>
 
                    (a) ThyssenKrupp AG<br>
                    (b) ArcelorMittal S.A.<br>
                    (c) Hebei Iron and Steel Group
                    <br><br>
                    and many others.
                </div>

                <div v-else-if="selectedDataset_graph2=='Automotive Branch'"> <!-- Was Automotive Stock -->
                    <h4 class="title incode">Automotive Branch</h4>
                    <!-- The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br> -->
                    
                    The selected Automotive Branch data set comprises a feature set of
                    the currently most important automitive companies. In particular, it contains stock market data from 9 companies such as<br><br>

                    (a) BMW<br>
                    (b) Toyota<br>
                    (c) TESLA
                    <br><br>
                    and many others.
                </div>

                <div v-else-if="selectedDataset_graph2=='Telecom Branch'"> <!-- Was Telecom Stock -->
                    <h4 class="title incode">Telecom Branch</h4>
                    <!-- The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br> -->
                    
                    The selected Telecom Branch data set comprises a feature set of the
                    currently most important telecom companies. In particular, it contains stock market data from 13 companies such as<br><br>

                    (a) AT&amp;T<br>
                    (b) Vodafone Group<br>
                    (c) China Mobile
                    <br><br>
                    and many others.
                </div>

                <div v-else-if="selectedDataset_graph2=='Tech Branch'"> <!-- Was Tech Stock -->
                    <h4 class="title incode">Tech Branch</h4>
                    <!-- The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br> -->

                    The selected Tech Branch data set comprises a feature set of the currently most important tech companies. In particular, it contains stock market
                    data from 21 companies such as<br><br>

                    (a) Alphabet<br>
                    (b) Apple<br>
                    (c) Netflix
                    <br><br>
                </div>
                
                <div v-else>
                    <h4 class="title incode">No dataset selected yet</h4>
                </div>

            </div>
            
        </div>

    </div>
</div>
</template>

<script>
//import { Tabs } from "@/components";
import Tabs from "./components/TabsSection";
import axios from 'axios'
import LineChart from './components/LineChart.vue'
import format from 'date-fns/format'

export default {
    components: {
        Tabs,
        LineChart
    },
    bodyClass: "profile-page",
    data() {
        let dateFormat = this.$material.locale.dateFormat || 'yyyy-MM-dd'
        let now = new Date()

        return {
            loading_graph1: false,
            loading_graph2: false,
            connection: false,
            start_date: format(now, dateFormat),
            end_date: format(now, dateFormat),
            selectedDataset_graph1: 'Select dataset',
            selectedDataset_graph2: 'Select dataset',
            dataset_axis_label: '',
            disabledDates: function (date) {
                // compare if today is greater than the datepickers date
            },
            dataset_id: '',
            chartdata: null,
            chartlabels: null,
            datecheck_bool: null,
            chart: {
                responsive: true,
                maintainAspectRatio: true,
                aspectRatio: 2
            }

        }
    },
    computed: {
        // eslint-disable-next-line

        dateFormat() {
            return this.$material.locale.dateFormat || 'yyyy-MM-dd'
        }
    },

    methods: {

        ping_server() {
            axios.post('http://localhost:5000/predict', {
                    ping: 1
                })
                .then(response => {

                    if (response.data.alive === 1) {
                        this.connection = true;
                        this.notifyVue('top', 'center', 'success', 'Connection to backend established.');

                    } else {
                        this.connection = false;
                        this.notifyVue('top', 'center', 'danger', 'Backend is not configured properly.');
                    }

                })
                .catch(e => {
                    this.notifyVue('top', 'center', 'danger', 'Connection failed. Backend is not responding.');

                })
        },

        notifyVue(verticalAlign, horizontalAlign, type_notification, notify_message) {
            var color = Math.floor(Math.random() * 4 + 1);
            this.$notify({
                message: notify_message,
                icon: "add_alert",
                horizontalAlign: horizontalAlign,
                verticalAlign: verticalAlign,
                type: type_notification
            });
        },
        select_set(selected_graph) {

            if(selected_graph == 1){
                this.loading_graph1 = true;
            }
            else{
                this.loading_graph2 = true;
            }
            
            axios.post('http://localhost:5000/predict', {
                    dataset_id_req: this.dataset_id,
                    selected_graph: selected_graph
                })
                .then(response => {

                    
                        this.acceptedRequest = response.data.class;
                        if( response.data.selected_graph == 1)
                        {
                            this.chartlabels_graph1 = response.data.labels,
                            this.chartdata_graph1 = [{
                                    label: 'ground truth',
                                    data: response.data.chart_data_1,
                                    borderColor: 'rgb(0, 0, 0)',
                                    fill: false,
                                    pointRadius: 0,
                                    borderWidth:2
                                },
                                {
                                    label: 'model data',
                                    data: response.data.chart_data_2,
                                    borderColor: 'rgb(112, 112, 112)',
                                    fill: false,
                                    pointRadius: 0,
                                    borderWidth:2
                                },
                                {
                                    label: 'prediction',
                                    data: response.data.chart_data_3,
                                    borderColor: '#e53935',
                                    fill: false,
                                    pointRadius: 0,
                                    borderWidth:2

                                }
                            ]
                        }

                        else if( response.data.selected_graph == 2)
                        {
                            this.chartlabels_graph2 = response.data.labels,
                            this.chartdata_graph2 = [{
                                    label: 'ground truth',
                                    data: response.data.chart_data_1,
                                    borderColor: 'rgb(0, 0, 0)',
                                    fill: false,
                                    pointRadius: 0,
                                    borderWidth:2
                                },
                                {
                                    label: 'model data',
                                    data: response.data.chart_data_2,
                                    borderColor: 'rgb(112, 112, 112)',
                                    fill: false,
                                    pointRadius: 0,
                                    borderWidth:2,
                                },
                                {
                                    label: 'prediction',
                                    data: response.data.chart_data_3,
                                    borderColor: '#e53935',
                                    fill: false,
                                    pointRadius: 0,
                                    borderWidth:2
                                }
                            ]
                        }
                        
                        this.datecheck_bool = response.data.datecheck;
                        if(selected_graph == 1){
                            this.loading_graph1 = false;
                        }
                        else{
                            this.loading_graph2 = false;
                        }
                        this.checkdate(this.datecheck_bool);
                })
                .catch(e => {
                    this.loading_graph1 = false,
                    this.loading_graph2 = false,
                    this.notifyVue('top', 'center', 'danger', 'Connection failed.');
                    
                    
                })

        },
        toString() {
            this.toDate()
            this.dynamicByModel = this.dynamicByModel && format(this.dynamicByModel, this.dateFormat)
        },
        disableTo(val) {
            if (typeof this.disabled.to === "undefined") {
                this.disabledDates = {
                    to: null,
                    daysOfMonth: this.disabledDates.daysOfMonth,
                    from: this.disabled.from
                };
            }
            this.disabledDates.to = val;
        },
        checkdate(bool) {
            if (bool == 1) {
                this.notifyVue('top', 'center', 'danger', 'End-date > Start-date.');
            }
        },
        disableFrom(val) {
            if (typeof this.disabledDates.from === "undefined") {
                this.disabled = {
                    to: this.disabledDates.to,
                    daysOfMonth: this.disabled.daysOfMonth,
                    from: null
                };
            }
            this.disabledDates.from = val;
        }

    },
    mounted() {
        //executed after page is loaded -> see vue component lifeciycle
        this.ping_server();
        //this.select_set();

    },

    props: {
        header: {
            type: String,
            default: require("@/assets/img/background.jpg")

        }
    },
    computed: {
        headerStyle() {
            return {
                backgroundImage: `url(${this.header})`
            };
        }
    }
};


</script>

<style lang="scss" scoped>

html {
  scroll-behavior: smooth;
}

.section {
    padding: 0;
}

.profile-tabs::v-deep {
    .md-card-tabs .md-list {
        justify-content: left;
    }

    [class*="tab-pane-"] {
        margin-top: 3.213rem;
        padding-bottom: 50px;

        img {
            margin-bottom: 2.142rem;
        }
    }
}

.menuu {
    margin-right: 5em;
    margin-top: 0.15em;
}

.code {
    background: rgb(40, 44, 52);
    color: #fff;
    margin: 2em;
    padding: 2em;
    border-radius: 0.4em;
    webkit-box-shadow: 0px 0px 25px 0px rgba(0, 0, 0, 0.39);
    -moz-box-shadow: 0px 0px 25px 0px rgba(0, 0, 0, 0.39);
    box-shadow: 0px 0px 25px 0px rgba(0, 0, 0, 0.39);
}

.incode {
    color: #fff;
    margin-top: 0;
}

.main-raised {
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}

.controls {
    margin-top: 50px;
    margin-bottom: 10px;

}


/* chart */

.top-pinned {
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 9000;
    background: transparent
}

/* page */
.profile-page {
    .page-header {
        height: 180px;
        background-position: center center;

        &::before {
            background: rgba(0, 0, 0, .2);
        }
    }

}

.fsize-chart {
    margin-top: 35px;
    width: 100%;
}

.fullwidth {
    width: 100%
}

.fixed-width-button {
    width: 16em;
}

.profile-content
{
    padding-bottom: 9px;
}

.loading-banner img{
width: 50%;
}
.loading-banner{
height: 400px;
text-align: center;
}

.no-margin
{
    margin-bottom: -25px;
}
</style>



