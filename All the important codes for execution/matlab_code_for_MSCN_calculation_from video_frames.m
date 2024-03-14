
    img_folder = dir('C:\Users\Krishna Baghel\Desktop\sample dataset ugc_images\UGC0001_720x1280_30_crf_00\*.jpg');
    for n= 1:length(img_folder)
        fname=strcat('C:\Users\Krishna Baghel\Desktop\sample dataset ugc_images\UGC0001_720x1280_30_crf_00\',img_folder(i).name);
        img= imread(fname)
    if(size(img,3)==3)
        img = rgb2gray(img);
    end

    if(isa(img,'uint8'))
        img = im2double(img);
    end

    window = fspecial('gaussian',7,7/6); 
    window = window/sum(sum(window));
   
    mu = filter2(window, img, 'same');
    mu_sq = mu.*mu;

    sigma = sqrt(abs(filter2(window, img.*img, 'same') - mu_sq));
    imgMinusMu = (img-mu);

    MSCN_im=imgMinusMu./(sigma +1);
    MSCN_img=[mean2(MSCN_im),std2(MSCN_im)];
    
    end

