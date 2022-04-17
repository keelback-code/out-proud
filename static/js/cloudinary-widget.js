function showUploadWidget() {
    cloudinary.openUploadWidget({
       cloudName: "<cloud name>",
       uploadPreset: "<upload preset>",
       sources: [
           "local",
           "url",
           "image_search"
       ],
       googleApiKey: "<image_search_google_api_key>",
       showAdvancedOptions: false,
       cropping: false,
       multiple: true,
       defaultSource: "local",
       styles: {
           palette: {
               window: "#4C0E4C",
               sourceBg: "#3A0A3A",
               windowBorder: "#AD5BA3",
               tabIcon: "#ffffcc",
               inactiveTabIcon: "#FFD1D1",
               menuIcons: "#FFD1D1",
               link: "#ffcc33",
               action: "#ffcc33",
               inProgress: "#00e6b3",
               complete: "#a6ff6f",
               error: "#ff1765",
               textDark: "#3c0d68",
               textLight: "#fcfffd"
           },
           fonts: {
               default: null,
               "'Fira Sans', sans-serif": {
                   url: "https://fonts.googleapis.com/css?family=Fira+Sans",
                   active: true
               }
           }
       }
   },
    (err, info) => {
      if (!err) {    
        console.log("Upload Widget event - ", info);
      }
     });
    }