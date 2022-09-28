function ig_out = fnc_filter(img, kernel)

[rows, cols, channels] = size(img);

img_out = zeros(rows, cols, channels);

img = double(img);

padding = floor(size(kernel, 1)) / 2;

for id_chn = 1:channels
	for id_row=(1 + padding):(rows - padding)
		for id_col = (1 + padding):(cols - padding)
			filter_value = 0
			for idx_ker = -padding:padding
				for idy_ker=-padding:padding
					filter_value = filter_value + img(id_row + idx_ker, id_col + idy_ker) * kernel(idx_ker + padding + 1, idy_ker + padding + 1);
				end
			end
		img_out(id_row, id_col, id_chn) = filter_value;
		end
	end
end

img_out = uint8(img_out);

end
