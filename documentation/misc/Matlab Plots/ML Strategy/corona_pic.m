%% Parameters

% Clear
clear all;
close all;
clc;

% Corona Factor
factor = 1.7;

% Range
x = 0: 0.1: 365; 
x_corona_start = 95;

% Outputs
prediction = 0.12*x + 10 + (1.7*log(1 - x.^2)) + 0.8 .* sin(2*pi*0.05*x) + (1.7*log(x.^2)).^(-1);
reality = [prediction(1:x_corona_start), factor * prediction(x_corona_start+1:end)];
elements = size(reality, 2);

% Noise
noise = 6* rand(1, elements);
real_output_distorted = real(reality + noise);
model_output_distorted = real(prediction + noise);

% Error
error = real_output_distorted - model_output_distorted;

% Line Values
x_val = 180;
x_index = find(x==x_val);
y1 = model_output_distorted(x_index);
y2 = real_output_distorted(x_index);

x_val_start = x(x_corona_start);
y1_start = model_output_distorted(x_corona_start); 
y2_start = real_output_distorted(x_corona_start+3);

%% Plot
figure
plot(x, real_output_distorted, x, model_output_distorted)
line([x_val x_val],[y1 y2], 'linewidth', 2, 'color', 'red')

text(180, y1 + (y2-y1)*0.5, '\leftarrow \Delta Corona')
text(x_val_start, y1_start + (y2_start-y1_start)*0.5, '\leftarrow Surge')

xlim([0 365])
ylim([0 170])
xlabel('Days since Lockdown')
ylabel('New Subscribers')
title('Streaming During Corona')
legend('Reality','Model Prediction')
grid on

% Tightfig
h = gcf; 
tightfig(h)




