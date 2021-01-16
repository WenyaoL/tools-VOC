from DateAugmentLabelImg.DataAugmentVOC import DataAugmentVOC
from concurrent.futures import ProcessPoolExecutor,wait

def multiprocessAug(args):
    V = DataAugmentVOC(rootpath=args.root_path)
    executor = ProcessPoolExecutor(max_workers=5)
    f_list = []
    if args.xmlpath is not None:
        V.setSave_xmlpath(args.xmlpath)
    if args.imgpath is not None:
        V.setSave_imgpath(args.imgpath)
    if args.hub is not None:
        # hub 0~180   sat 0~2   val 0~2
        f_list.append(executor.submit(V.changeHsv, hub=args.hub, sat=args.sat, val=args.val))
    if args.rotate is not None:
        f_list.append(executor.submit(V.rotate, args.rotate))
    if args.Noise is True:
        f_list.append(executor.submit(V.addNoise))
    if args.changeLight is True:
        f_list.append(executor.submit(V.changeLight))
    if args.filp is True:
        f_list.append(executor.submit(V.filp, 1))

    wait(f_list)
    print('All subprocesses done.')
