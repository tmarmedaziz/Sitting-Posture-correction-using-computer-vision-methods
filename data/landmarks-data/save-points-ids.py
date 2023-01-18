from collections import ChainMap
import json

landmarks = "0. nose/1. lefteye_inner/2. left eye/3. left_eye_outer/4. right eye_inner/5. right_eye/6. " \
            "righteye_outer/7. left " \
            "ear/8. rightear/9. mouth left/10. mouth_right/11. left shoulder/12. right shoulder/13. left elbow/14. " \
            "right_elbow/15. left_wrist/16. rightwrist/17. leftpinky/18. rightpinky/19. leftindex/20. right_index/21. " \
            "left_thumb/22. right thumb/23. left_hip/24. right hip/25. left_knee/26. right knee/27. leftankle/28. " \
            "right ankle/29. " \
            "left heel/30. rightheel/31. left foot_index/32. right footindex "

dictionaries = [{elt.split(". ")[1]: int(elt.split(". ")[0])} for elt in landmarks.split("/")]

points_landamrks = dict(ChainMap(*dictionaries))
with open('landmarks-labels.json', 'w') as fp:
    json.dump(points_landamrks, fp)
