<template>
  <div class="wrapper">
    <div id="nav-tabs">
      <div class="md-layout">
        <div class="md-layout-item md-size-100 md-small-size-100">
          <nav-tabs-card no-label tabs-plain>
            <template slot="content">
              <md-tabs class="md-danger" 
                       md-alignment="center">
                  <md-tab id="tab-home" 
                          md-label="Welcome">
                    <div class="text-alignment">
                      
                      <p>The COVID-19 pandemic has affected our everyday lives to a huge extent. 
                      More often than not, we wonder <b>what</b> the world would have looked like <b>if</b> the pandemic actually never happened.
                      </p>
                      <p>
                      Using <b>what_if.ai</b>, two of the most impactful driving factors of the modern world - our <b>global 
                      economy</b> and <b>internet traffic</b> behavior - are modeled and predicted for a scenario without COVID-19. 
                      It allows you to observe the influence of the pandemic and analyzes whether the common assumption, 
                      that the surge in internet traffic has solely benefited the technology sector, holds true. 
                      </p>
                      <br>
                      <p style="font-size:24px;text-align:center;">
                      <b>Are you excited for an insight?</b>
                      </p>
                      <br>
                      <div style="position:relative;padding-top:56.25%;">
                        <iframe src="https://www.youtube.com/embed/AChsZ0fCOjk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;"></iframe>
                      </div>
                      
                    </div>
                  </md-tab>
                  <md-tab id="tab-how-to" 
                          md-label="How to use what_if.ai">
                    <div class="text-alignment">
                      <p>
                        In order to model and eventually compare <b>global economic</b> and <b>online activity trends</b>, what if.ai provides many different data sets to choose from. 
                        These range from <b>stock market projections</b> for industry branches such as the medical and tech one, to <b>more specific metrics</b> as internet exchange point bitrates 
                        and streaming statistics which describe the online activity in form of internet traffic.               
                      </p>
                      <br>
                      <l>
                      Simply select your desired data set and let the <b>AI model</b> do its magic.
                      The resulting <b>model prediction</b> is displayed in green alongside the original
                      true data in red.
                      </l>
                    </div>
                  </md-tab>
                  <md-tab id="tab-about-the-model" md-label="About the AI Model">
                    <div class="text-alignment">
                      <img src="./../../assets/fb_pro.png" 
                           style="float:right;width:300px;height:100px;margin:16px;"/>
                      <p>
                        The main goal of the what if.ai project is to forecast time series for the
                        respective data sets. To this, we prefer to use <b>Prophet</b>, a forecasting
                        framework provided by Facebook.<br><br>

                        Prophet is based on an <b>additive model composition</b> where non-linear trends
                        are being fit with either yearly, weekly or daily seasonality. As such, it
                        perfectly suits our time series modeling task. Furthermore, it promises to
                        be especially robust to missing data or shifts in the trend itself and thus
                        handles outliers very well.<br><br>
                        <b>How it works</b><br><br>
                        Prophet is an additive regression model with four main components:<br>
                      <p/>
                      <ul>
                        <li>A piecewise linear or logistic growth curve trend
                          (Detects changes in trends automatically by selecting changepoints
                          from the data)</li>
                        <li>A yearly seasonal component modeled using Fourier series</li>
                        <li>A weekly seasonal component using dummy variables</li>
                        <li>A user-provided list of important events (i.e. holidays, etc.)</li>
                      </ul>
                      <p>
                        The main idea is to very <b>flexibly fit the trend component</b> which leads to
                        a better identification of the model seasonality and thus a more <b>accurate
                        forecast</b>. This is done by choosing a flexible curve-fitting like regression
                        model instead of more traditional time series models.<br><br>

                        The Prophet model is eventually fitted using <a href="https://mc-stan.org/"> <b>Stan</b></a> which performs a <b>MAP
                        optimization</b> for the respective parameters. Additionally, this allows for
                        a parameter uncertainty estimation using the Hamiltonian Monte Carlo
                        algorithm.<br><br>
                      </p>
                    </div>
                  </md-tab>
                  <md-tab id="tab-anal" md-label="Analysis">
                    <div class="text-alignment">
                      <img src="./../../assets/corona.png" alt="Corona" style="float:left;margin:16px;width:300px;height:150px;"/>
                      <br />
                      <p>
                        The discrepancies between our <b>modeled courses</b> and the <b>actual observations </b>
                        strongly suggest that the pandemic had a major impact on internet consumption 
                        by <b>increasing traffic</b> across a wide variety of platforms. We interpret 
                        this as a consequence of government enforced lockdowns all around the world, 
                        eventually forcing people to increasingly rely on home office and online entertainment. 
                      </p>
                      <br />
                      <p>
                      As a further consequence of the lockdowns, all economic sectors we look at took a <b>huge blow</b>. 
                      We attribute this to the fear of the economic impact of the pandemic spreading across the markets. 
                      Surprisingly, some traditional industries like the steel sector were less 
                      affected than we initially thought. We are unsure as to why that is, but one reason could be that 
                      branches not directly related to the consumer market are less bound to immediate consumer decisions, 
                      and are thus more likely to be bound to delivery contracts in the industrial sector.   
                      </p>
                      <br />
                      <p>
                      Also, counter to the common narrative, the tech sector <b>wasn’t the only sector to make a speedy 
                      recovery</b> once the initial shock was over. 
                      We take this as an indication that, although certainly a contributing factor, 
                      the shift towards online communication and entertainment is <b>not the main driver</b> 
                      constituting a rapid rehabilitation.
                      </p>
                    </div>
                  </md-tab>
                  <md-tab id="tab-meet-the-team" md-label="Meet the Team" style="margin:16px;">
                    <div class="text-alignment">
                      <img src="./../../assets/team.jpeg" alt="Legends of tomorrow =)" />
                      <br/>
                      <br>
                      <p>
                        The team behind what if.ai is composed of 9 extraordinary individuals
                        that took time and effort during the extremely demanding COVID-19
                        pandemic to organize and eventually implement a successful model which
                        suffices to predict time series as desired.
                      </p>
                    </div>
                  </md-tab>
              </md-tabs>
            </template>
          </nav-tabs-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { NavTabsCard } from "@/components";

export default {
  components: {
    NavTabsCard
  }
};
</script>

<style lang="css">

.text-alignment{
  text-align: left;
  margin: 16px;
}

</style>
