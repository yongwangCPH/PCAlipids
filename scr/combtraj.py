import mdtraj as md
import numpy as np
from multiprocessing import Pool


def load_traj(traj_file, top_file):
	traj = md.load_xtc(traj_file, top_file)
	return traj


def average_structure(traj):
	avg_xyz = traj.xyz.astype(np.float64)
	avg_xyz = avg_xyz.mean(axis = 0, dtype=np.float64)
	avg_traj = md.Trajectory([avg_xyz], traj.top)
	return avg_traj


def main(data):
	with Pool(2) as p:
		trajs = p.starmap(load_traj, data)
	traj = trajs[0]
	length = [len(trajs[0]), len(trajs[1])]
	for i in range(1, len(trajs)):
		traj = traj.join(trajs[i])
		trajs[i] = 0
	traj = traj.superpose(traj[0], parallel = True)
	avg_str = average_structure(traj)
	traj = traj.superpose(avg_str, parallel = True)
	traj[:length[0]].save_xtc('concatenated1_FALL.xtc')
	average_structure(traj[:length[0]]).save('average1_FALL.pdb')
	traj[length[0]:].save_xtc('concatenated2_FALL.xtc')
	average_structure(traj[length[0]:]).save('average2_FALL.pdb')
	avg_str = average_structure(traj)
	traj.save_xtc('united.xtc')
	avg_str.save('average.pdb')


# if __name__ == '__main__':
# 	args = sys.argv[1:]
# 	i = 0
# 	data = []
# 	while i < len(args):
# 		if args[i] == '-fs':
# 			data.append((args[i + 1], args[i + 2]))
# 			i += 3
# 	main(data)