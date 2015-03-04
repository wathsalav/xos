def handle(image):
    print ">>>>>>>>>>>>>> POLICY_HANDLE"
    from core.models import Controller, ControllerImages, Image
    from collections import defaultdict

    controller_images = ControllerImages.objects.filter(image=image)
    existing_controllers = [cs.controller for cs in controller_images] 
    
    all_controllers = Controller.objects.all() 
    print "controller: %s"%existing_controllers
    print "all_controllers: %s"%all_controllers
    for controller in all_controllers:
        if controller not in existing_controllers:
            sd = ControllerImages(image=image, controller=controller)
            sd.save()

